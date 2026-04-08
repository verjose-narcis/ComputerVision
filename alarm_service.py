
import pygame


def init_alarm(sound_path):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)


def start_alarm(alarm_playing):
    if not alarm_playing:
        pygame.mixer.music.play(-1)
        return True
    return alarm_playing


def stop_alarm(alarm_playing):
    if alarm_playing:
        pygame.mixer.music.stop()
        return False
    return alarm_playing