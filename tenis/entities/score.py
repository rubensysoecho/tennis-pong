import pygame
from tenis.entities.paddle import PaddleType

class Score:    
    def __init__(self, score, font):
        self.score = score 
        self.won = False
        self.win_text = None              
        self.__font = font
        
    def render(self, screen, paddle_side, screen_size, color):
        self.__score_text = self.__font.render(f"{self.score}", 1, color)
        if paddle_side == PaddleType.Left:
            screen.blit(self.__score_text, (screen_size[0]//4-self.__score_text.get_width()//2, 20))
        elif paddle_side == PaddleType.Right:
            screen.blit(self.__score_text, (screen_size[0]*(3/4)-self.__score_text.get_width()//2, 20))        

    def update(self):
        self.score += 1
    
    def reset(self):
        self.score = 0
        self.won = False
        self.win_text = None
