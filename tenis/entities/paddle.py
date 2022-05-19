import pygame
from enum import Enum

class PaddleType(Enum):
    Right = "right",
    Left = "left"

class Paddle:    
    def __init__(self, x, y, size, speed, color):        
        self.x = x
        self.y = y
        self.position = pygame.math.Vector2(x, y)
        self.moving_up = False
        self.moving_down = False
        self.width = size[0]
        self.height = size[1]
        self.speed = speed
        self.color = color

    def update(self, delta_time, screen_size):
        movement = pygame.math.Vector2(0.0, 0.0)
        if self.moving_up:
            movement.y -= self.speed
        elif self.moving_down:
            movement.y += self.speed
        self.position += movement * delta_time
        self.check_bounds(screen_size)

    def render(self, win):
        pygame.draw.rect(win, self.color, (self.position.x, self.position.y, self.width, self.height))                

    def reset(self, paddle_size):
        self.position = pygame.math.Vector2(self.x, self.y)
        self.width = paddle_size[0]
        self.height = paddle_size[1]
        self.moving_down = False
        self.moving_up = False
                