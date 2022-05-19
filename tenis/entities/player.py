from tenis.entities.paddle import Paddle
import pygame

class Player(Paddle):
    def __init__(self, x, y, size, speed, color):
        super().__init__(x, y, size, speed, color)
        self.win_text = None
        
    def check_bounds(self, screen_size):
        if self.position.y <= 0:
            self.position.y = 0
        if self.position.y >= screen_size[1] - self.height:
            self.position.y = screen_size[1] - self.height

        
    def handle_colision(self, ball, screen_size):
        if ball.position.y + ball.radius >= screen_size[1] or ball.position.y - ball.radius <= 0:
            ball.y_vel *= -1

        if self.position.y <= ball.position.y <= self.position.y + self.height:                
                if ball.position.x - ball.radius <= self.position.x + self.width:             
                    ball.x_vel *= -1

                    middle_y = self.position.y + self.height / 2
                    difference_in_y = middle_y - ball.position.y
                    reduction_factor = (self.height / 2) / ball.speed
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel 
                    return True

