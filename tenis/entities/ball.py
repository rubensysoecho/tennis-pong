import pygame

class Ball:    
    def __init__(self, x, y, radius, speed, color):
        self.x = x
        self.y = y
        self.position = pygame.math.Vector2(x, y)
        self.radius = radius
        self.speed = speed
        self.x_vel = self.speed
        self.y_vel = 0
        self.__color = color

    def update(self):
        self.position.x += self.x_vel
        self.position.y += self.y_vel

    def render(self, surface_dest):
        pygame.draw.circle(surface_dest, self.__color, (self.position.x, self.position.y), self.radius)

    def handle_colision(self, left_paddle, right_paddle, screen_size):
        if self.position.y + self.radius >= screen_size[1] or self.position.y - self.radius <= 0:
            self.y_vel *= -1        

        if self.x_vel < 0:
            if self.position.y >= left_paddle.position.y and self.position.y <= left_paddle.position.y + left_paddle.height:
                if self.position.x - self.radius <= left_paddle.position.x + left_paddle.width:             
                    self.x_vel *= -1

                    middle_y = left_paddle.position.y + left_paddle.height / 2
                    difference_in_y = middle_y - self.position.y
                    reduction_factor = (left_paddle.height / 2) / self.speed
                    y_vel = difference_in_y / reduction_factor
                    self.y_vel = -1 * y_vel 
                    return True  

        else:
            if self.position.y >= right_paddle.position.y and self.position.y <= right_paddle.position.y + right_paddle.height:
                if self.position.x + self.radius >= right_paddle.position.x:                    
                    self.x_vel *= -1

                    middle_y = right_paddle.position.y + right_paddle.height / 2
                    difference_in_y = middle_y - self.position.y
                    reduction_factor = (right_paddle.height / 2) / self.speed
                    y_vel = difference_in_y / reduction_factor
                    self.y_vel = -1 * y_vel
                    return True
        return False

    def reset(self):
        self.position = pygame.math.Vector2(self.x, self.y)
        self.y_vel = 0
        self.x_vel *= -1