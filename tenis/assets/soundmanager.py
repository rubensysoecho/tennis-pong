from importlib import resources
from tenis.config import cfg_item
import pygame

class SoundMannager:
    __instance = None
    
    @staticmethod
    def instance():
        if SoundMannager.__instance is None:
            SoundMannager()
        return SoundMannager.__instance 

    def __init__(self):
        if SoundMannager.__instance is None:
            SoundMannager.__instance = self

            self.__sound_volume = cfg_item("sfx", "volume")
            self.__music_volume = cfg_item("music", "volume")

            self.__current_music = None
            self.__next_music = None
        else:
            raise Exception("SoundManager doesn't allow multiple instances")

    def play_sound(self, file):
        with resources.path(*file) as audio_file:
            sound = pygame.mixer.Sound(audio_file)
        sound.set_volume(self.__sound_volume)
        sound.play()

    def play_music(self, file):
        if file is self.__current_music:
            return        
        with resources.path(*file) as music_file:            
            pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(self.__music_volume)
        self.__current_music = file
        pygame.mixer.music.play(-1)
        
