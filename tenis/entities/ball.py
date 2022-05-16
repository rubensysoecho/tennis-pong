import pygame

class Ball:    
    def __init__(self, x, y, radius, speed, color):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.speed = speed
        self.x_vel = self.speed
        self.y_vel = 0
        self.__color = color

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def render(self, surface_dest):
        pygame.draw.circle(surface_dest, self.__color, (self.x, self.y), self.radius)

    def handle_colision(self, left_paddle, right_paddle, screen_size):
        if self.y + self.radius >= screen_size[1] or self.y - self.radius <= 0:
            self.y_vel *= -1        

        if self.x_vel < 0:
            if self.y >= left_paddle.y and self.y <= left_paddle.y + left_paddle.height:
                if self.x - self.radius <= left_paddle.x + left_paddle.width:             
                    self.x_vel *= -1

                    middle_y = left_paddle.y + left_paddle.height / 2
                    difference_in_y = middle_y - self.y
                    reduction_factor = (left_paddle.height / 2) / self.speed
                    y_vel = difference_in_y / reduction_factor
                    self.y_vel = -1 * y_vel 
                    return True  

        else:
            if self.y >= right_paddle.y and self.y <= right_paddle.y + right_paddle.height:
                if self.x + self.radius >= right_paddle.x:                    
                    self.x_vel *= -1

                    middle_y = right_paddle.y + right_paddle.height / 2
                    difference_in_y = middle_y - self.y
                    reduction_factor = (right_paddle.height / 2) / self.speed
                    y_vel = difference_in_y / reduction_factor
                    self.y_vel = -1 * y_vel
                    return True
        return False

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1