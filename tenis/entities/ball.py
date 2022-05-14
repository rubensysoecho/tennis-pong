import pygame
from tenis.config import cfg_item

class Ball:
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

        self.__color = cfg_item("object_color")

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def render(self, surface_dest):
        pygame.draw.circle(surface_dest, self.__color, (self.x, self.y), self.radius)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1