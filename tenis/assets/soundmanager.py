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

    def play_sound(self, name):
        with resources.path(*cfg_item("sfx", name, "audio_file")) as audio_file:
            sound = pygame.mixer.Sound(audio_file)
        sound.set_volume(self.__sound_volume)
        sound.play()

    def play_music(self, name):
        if name is self.__current_music:
            return
        
        with resources.path(*cfg_item("music", name, "audio_file")) as music_file:            
            pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(self.__music_volume)
        self.__current_music = name
        pygame.mixer.music.play(-1)
        
