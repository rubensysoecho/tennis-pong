import pygame
from enum import Enum

class PaddleType(Enum):
    Right = "right",
    Left = "left"

class Paddle:
    VEL = 4

    def __init__(self, x, y, size, speed, color):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = size[0]
        self.height = size[1]
        self.speed = speed

        self.__color = color

    def update(self, up=True):
        if up:
            self.y -= self.speed
        else:
            self.y += self.speed

    def render(self, win):
        pygame.draw.rect(win, self.__color, (self.x, self.y, self.width, self.height))                

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y