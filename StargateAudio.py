import pygame


class StargateAudio:
    def __init__(self):
        pygame.mixer.init(44100, -16, 2, 2048)

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def play_roll(self):
        pygame.mixer.stop()
        pygame.mixer.music.load('audio/roll.mp3')
        pygame.mixer.music.play()

    def stop_roll(self):
        pygame.mixer.music.fadeout(200)
        while pygame.mixer.music.get_busy():
            continue

    def play_chevron_lock(self):
        pygame.mixer.music.load('audio/chev1.mp3')
        pygame.mixer.music.play()

    def play_chevron_unlock(self):
        pygame.mixer.music.load('audio/chev2.mp3')
        pygame.mixer.music.play()

    def play_open(self):
        pygame.mixer.stop()
        pygame.mixer.music.load('audio/open.mp3')
        pygame.mixer.music.play()

    def play_close(self):
        pygame.mixer.stop()
        pygame.mixer.music.load('audio/close.mp3')
        pygame.mixer.music.play()

    def play_theme(self):
        pygame.mixer.stop()
        pygame.mixer.music.load('audio/sg1thm.mp3')
        pygame.mixer.music.play()
