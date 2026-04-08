import os
import time
import cv2
import mediapipe as mp

import config
from metrics import calculate_ear, calculate_mar
from state_manager import DrowsinessState
from alerts import (
    send_absence_alert,
    check_absence_alert,
    check_fatigue_alert,
    build_absence_whatsapp_message,
    build_fatigue_whatsapp_message
)
from whatsapp_service import create_twilio_client, send_whatsapp_to_many
from draw import draw_points, draw_detection_info, draw_absence_info
from alarm_service import init_alarm, start_alarm, stop_alarm


def get_point_float(face_landmarks, idx, w, h):
    landmark = face_landmarks.landmark[idx]
    x = landmark.x * w
    y = landmark.y * h
    return (x, y)


def get_point_int(face_landmarks, idx, w, h):
    x, y = get_point_float(face_landmarks, idx, w, h)
    return (int(x), int(y))


def main():
    init_alarm(config.ALARM_SOUND_PATH)

    twilio_client = None

    if config.ENABLE_WHATSAPP_ALERTS:
        twilio_client = create_twilio_client(
            config.TWILIO_ACCOUNT_SID,
            config.TWILIO_AUTH_TOKEN
        )

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    print("Abriendo cámara...")
    cap = cv2.VideoCapture(config.CAMERA_INDEX, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("ERROR: no se pudo abrir la cámara")
        return

    print("OK cámara")
    print("Presiona Q para salir")

    state = DrowsinessState()
    alarm_playing = False

    absence_start_time = None
    absence_alert_sent = False
    absence_whatsapp_sent_once = False
    absence_seconds = 0

    fatigue_alert_sent = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: no se pudo leer frame")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        h, w, _ = frame.shape
        absence_alert_active = False
        fatigue_alert_active = False

        if results.multi_face_landmarks:
            absence_start_time = None
            absence_alert_sent = False
            absence_seconds = 0

            face_landmarks = results.multi_face_landmarks[0]

            draw_points(frame, face_landmarks, config.LEFT_EYE, w, h, get_point_int, (0, 255, 0))
            draw_points(frame, face_landmarks, config.RIGHT_EYE, w, h, get_point_int, (255, 0, 0))
            draw_points(frame, face_landmarks, config.MOUTH, w, h, get_point_int, (0, 0, 255))

            left_ear = calculate_ear(face_landmarks, config.LEFT_EYE, w, h, get_point_float)
            right_ear = calculate_ear(face_landmarks, config.RIGHT_EYE, w, h, get_point_float)
            avg_ear = (left_ear + right_ear) / 2.0
            mar = calculate_mar(face_landmarks, config.MOUTH, w, h, get_point_float)

            current_eye_state, eye_color, microsleep_active = state.update_eyes(avg_ear, config)
            current_mouth_state, mouth_color = state.update_mouth(mar, config)

            fatigue_alert_active = check_fatigue_alert(
                state.microsleep_count,
                config.FATIGUE_MICROSLEEP_THRESHOLD
            )

            if microsleep_active:
                alarm_playing = start_alarm(alarm_playing)
            else:
                alarm_playing = stop_alarm(alarm_playing)

            if fatigue_alert_active and not fatigue_alert_sent:
                if config.ENABLE_WHATSAPP_ALERTS and twilio_client is not None:
                    body = build_fatigue_whatsapp_message(state.microsleep_count)

                    try:
                        results = send_whatsapp_to_many(
                            twilio_client,
                            config.TWILIO_WHATSAPP_FROM,
                            config.TWILIO_WHATSAPP_TO,
                            body
                        )

                        for number, sid in results:
                            print(f"WhatsApp de fatiga enviado a {number}. SID: {sid}")

                    except Exception as e:
                        print(f"Error enviando WhatsApp de fatiga: {e}")

                fatigue_alert_sent = True

            draw_detection_info(
                frame,
                avg_ear,
                mar,
                current_eye_state,
                eye_color,
                current_mouth_state,
                mouth_color,
                state.eye_event_text,
                state.mouth_event_text,
                state.blink_count,
                state.yawn_count,
                state.microsleep_count,
                alarm_playing,
                fatigue_alert_active
            )

        else:
            if absence_start_time is None:
                absence_start_time = time.time()

            absence_seconds = int(time.time() - absence_start_time)

            if check_absence_alert(absence_seconds, config.ABSENCE_THRESHOLD_SECONDS):
                absence_alert_active = True

                if not absence_alert_sent:
                    send_absence_alert()
                    absence_alert_sent = True

                if (
                    not absence_whatsapp_sent_once
                    and config.ENABLE_WHATSAPP_ALERTS
                    and twilio_client is not None
                ):
                    body = build_absence_whatsapp_message(absence_seconds)

                    try:
                        results = send_whatsapp_to_many(
                            twilio_client,
                            config.TWILIO_WHATSAPP_FROM,
                            config.TWILIO_WHATSAPP_TO,
                            body
                        )

                        for number, sid in results:
                            print(f"WhatsApp de ausencia enviado a {number}. SID: {sid}")

                        absence_whatsapp_sent_once = True

                    except Exception as e:
                        print(f"Error enviando WhatsApp de ausencia: {e}")

            alarm_playing = stop_alarm(alarm_playing)
            draw_absence_info(frame, absence_seconds, absence_alert_active)

        cv2.imshow(config.WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    stop_alarm(alarm_playing)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()