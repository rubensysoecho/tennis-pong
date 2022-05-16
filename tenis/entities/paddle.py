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
        self.win_text = None

    def update(self, delta_time, screen_size):
        movement = pygame.math.Vector2(0.0, 0.0)
        if self.moving_up:
            movement.y -= self.speed
        elif self.moving_down:
            movement.y += self.speed
        self.position += movement * delta_time
        self.check_bounds(screen_size)
        
    def check_bounds(self, screen_size):
        if self.position.y <= 0:
            self.position.y = 0
        if self.position.y >= screen_size[1] - self.height:
            self.position.y = screen_size[1] - self.height
    def render(self, win):
        pygame.draw.rect(win, self.color, (self.position.x, self.position.y, self.width, self.height))                

    def reset(self):
        self.position = pygame.math.Vector2(self.x, self.y)
        self.win_text = None