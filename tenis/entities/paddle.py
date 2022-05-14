import pygame
from tenis.config import cfg_item

class Paddle:
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

        self.__color = cfg_item("object_color")

    def update(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def render(self, win):
        pygame.draw.rect(win, self.__color, (self.x, self.y, self.width, self.height))

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y