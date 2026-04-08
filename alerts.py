
def send_absence_alert():
    print("ALERTA: Personal ausente en la estación por más de 10 minutos")


def check_absence_alert(absence_seconds, threshold_seconds):
    return absence_seconds >= threshold_seconds


def check_fatigue_alert(microsleep_count, threshold):
    return microsleep_count >= threshold


def build_absence_whatsapp_message(absence_seconds):
    return (
        """ Alerta de ausencia 
        Personal ausente o fuera de camara por mas de 10 min
        
        Favor de verificar la estacion."""
    )


def build_fatigue_whatsapp_message(microsleep_count):
    return (
        """ALERTA SafeFOCUS\n
        Se detectó fatiga en el personal."""
        f"Microsueños acumulados: {microsleep_count}."

    )