# draw.py

import cv2


def draw_points(frame, face_landmarks, indices, w, h, get_point_int, color):
    for idx in indices:
        x, y = get_point_int(face_landmarks, idx, w, h)
        cv2.circle(frame, (x, y), 2, color, -1)


def draw_text(frame, text, position, color=(255, 255, 255), scale=0.7, thickness=2):
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        thickness
    )


def draw_detection_info(
    frame,
    avg_ear,
    mar,
    current_eye_state,
    eye_color,
    current_mouth_state,
    mouth_color,
    eye_event_text,
    mouth_event_text,
    blink_count,
    yawn_count,
    microsleep_count,
    alarm_playing,
    fatigue_alert_active,
):
  
    draw_text(frame, current_eye_state, (20, 35), eye_color, 0.7)
    draw_text(frame, current_mouth_state, (20, 65), mouth_color, 0.7)

    draw_text(frame, f"Parpadeos: {blink_count}", (20, 250), (255, 255, 255), 0.7)
    draw_text(frame, f"Bostezos: {yawn_count}", (20, 280), (255, 255, 255), 0.7)
    draw_text(frame, f"Microsuenos: {microsleep_count}", (20, 310), (0, 0, 255), 0.7)

    alarm_text = "ALARMA ACTIVADA" if alarm_playing else "Alarma inactiva"
    alarm_color = (0, 0, 255) if alarm_playing else (0, 255, 0)

    draw_text(frame, alarm_text, (20, 345), alarm_color, 0.8)

    if fatigue_alert_active:
        draw_text(
            frame,
            "ALERTA: Se detecto fatiga en el personal",
            (20, 380),
            (0, 0, 255),
            0.7
        )


def draw_absence_info(frame, absence_seconds, absence_alert_active):
    draw_text(frame, "No se detecta rostro", (20, 40), (0, 0, 255), 0.8)
    draw_text(frame, f"Ausencia: {absence_seconds} s", (20, 80), (0, 165, 255), 0.8)

    if absence_alert_active:
        draw_text(frame, 
                  "ALERTA: Personal ausente en estacion", 
                  (20, 120), 
                  (0, 0, 255),
                   0.8
        )