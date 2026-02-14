import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.load_sounds()
    
    def load_sounds(self):
        """Загрузка звуков"""
        pass
    
    def play_coin_sound(self):
        """Воспроизведение звука монеты"""
        pass
    
    def play_stomp_sound(self):
        """Воспроизведение звука топтания врага"""
        pass
    
    def play_jump_sound(self):
        """Воспроизведение звука прыжка"""
        pass
    
    def play_music(self):
        """Воспроизведение фоновой музыки"""
        self.music_playing = True
    
    def stop_music(self):
        """Остановка музыки"""
        self.music_playing = False
