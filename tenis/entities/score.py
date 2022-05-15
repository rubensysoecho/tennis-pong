from importlib import resources
import pygame
from tenis.config import cfg_item

class Score:    
    def __init__(self, score):
        self.score = score        
        with resources.path(*cfg_item("font", "file")) as font_file:
            self.__font = pygame.font.Font(font_file, cfg_item("font", "size"))
        
    def render(self):
        return self.__font.render(f"{self.score}", 1, cfg_item("object_color"))

    def update(self):
        self.score += 1
    
    def reset(self):
        self.score = 0
