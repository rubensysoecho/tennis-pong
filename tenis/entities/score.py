from importlib import resources
import pygame
from tenis.config import cfg_item
from tenis.entities.paddle import PaddleType

class Score:    
    def __init__(self, score):
        self.score = score 
        self.won = False
        self.win_text = ""       
        with resources.path(*cfg_item("font", "file")) as font_file:
            self.__font = pygame.font.Font(font_file, cfg_item("font", "size"))
        
    def render(self, screen, paddle_side):
        self.__score_text = self.__font.render(f"{self.score}", 1, cfg_item("object_color"))
        if paddle_side == PaddleType.Left:
            screen.blit(self.__score_text, (cfg_item("screen_size")[0]//4-self.__score_text.get_width()//2, 20))
        elif paddle_side == PaddleType.Right:
            screen.blit(self.__score_text, (cfg_item("screen_size")[0]*(3/4)-self.__score_text.get_width()//2, 20))        

    def update(self):
        self.score += 1
    
    def reset(self):
        self.score = 0
        self.won = False
        self.win_text = ""
