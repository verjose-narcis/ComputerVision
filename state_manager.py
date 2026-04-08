# state_manager.py

class DrowsinessState:
    def __init__(self):
        self.eye_closed_frames = 0
        self.yawn_frames = 0

        self.blink_count = 0
        self.yawn_count = 0
        self.microsleep_count = 0

        self.eye_event_text = "Sin evento"
        self.mouth_event_text = "Sin evento"

    def update_eyes(self, avg_ear, config):
        microsleep_active = False

        if avg_ear < config.EAR_THRESHOLD:
            self.eye_closed_frames += 1
        else:
            if config.BLINK_MIN_FRAMES <= self.eye_closed_frames < config.PROLONGED_EYE_CLOSURE_FRAMES:
                self.blink_count += 1
                self.eye_event_text = "Parpadeo detectado"
            elif config.PROLONGED_EYE_CLOSURE_FRAMES <= self.eye_closed_frames < config.MICROSLEEP_FRAMES:
                self.eye_event_text = "Cierre prolongado de ojos"
            elif self.eye_closed_frames >= config.MICROSLEEP_FRAMES:
                self.microsleep_count += 1
                self.eye_event_text = "MICROSUENO detectado"
            else:
                self.eye_event_text = "Ojos abiertos"

            self.eye_closed_frames = 0

        if avg_ear < config.EAR_THRESHOLD:
            if self.eye_closed_frames >= config.MICROSLEEP_FRAMES:
                current_eye_state = "MICROSUENO en curso"
                eye_color = (0, 0, 255)
                microsleep_active = True
            elif self.eye_closed_frames >= config.PROLONGED_EYE_CLOSURE_FRAMES:
                current_eye_state = "Cierre prolongado"
                eye_color = (0, 165, 255)
            else:
                current_eye_state = "Ojos cerrados"
                eye_color = (0, 255, 255)
        else:
            current_eye_state = "Ojos abiertos"
            eye_color = (0, 255, 0)

        return current_eye_state, eye_color, microsleep_active

    def update_mouth(self, mar, config):
        if mar >= config.YAWN_THRESHOLD:
            self.yawn_frames += 1
        else:
            if self.yawn_frames >= config.YAWN_MIN_FRAMES:
                self.yawn_count += 1
                self.mouth_event_text = "BOSTEZO detectado"
            elif mar >= config.MOUTH_OPEN_THRESHOLD:
                self.mouth_event_text = "Boca abierta"
            else:
                self.mouth_event_text = "Boca cerrada"

            self.yawn_frames = 0

        if mar >= config.YAWN_THRESHOLD:
            if self.yawn_frames >= config.YAWN_MIN_FRAMES:
                current_mouth_state = "BOSTEZO en curso"
                mouth_color = (0, 0, 255)
            else:
                current_mouth_state = "Posible bostezo"
                mouth_color = (0, 165, 255)
        elif mar >= config.MOUTH_OPEN_THRESHOLD:
            current_mouth_state = "Boca abierta"
            mouth_color = (0, 255, 255)
        else:
            current_mouth_state = "Boca cerrada"
            mouth_color = (255, 255, 255)

        return current_mouth_state, mouth_color