from multiprocessing import reduction
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

    def handle_colision(self, left_paddle, right_paddle):
        if self.y + self.radius >= cfg_item("screen_size")[1] or self.y - self.radius <= 0:
            self.y_vel *= -1        

        if self.x_vel < 0:
            if self.y >= left_paddle.y and self.y <= left_paddle.y + left_paddle.height:
                if self.x - self.radius <= left_paddle.x + left_paddle.width:
                    self.x_vel *= -1

                    middle_y = left_paddle.y + left_paddle.height / 2
                    difference_in_y = middle_y - self.y
                    reduction_factor = (left_paddle.height / 2) / self.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    self.y_vel = -1 * y_vel   

        else:
            if self.y >= right_paddle.y and self.y <= right_paddle.y + right_paddle.height:
                if self.x + self.radius >= right_paddle.x:
                    self.x_vel *= -1

                    middle_y = right_paddle.y + right_paddle.height / 2
                    difference_in_y = middle_y - self.y
                    reduction_factor = (right_paddle.height / 2) / self.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    self.y_vel = -1 * y_vel


    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1