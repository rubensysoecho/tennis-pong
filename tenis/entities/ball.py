import pygame

class Ball:    
    def __init__(self, x, y, radius, speed, added_speed, max_speed, color):
        self.x = x
        self.y = y
        self.position = pygame.math.Vector2(x, y)
        self.radius = radius
        self.speed = speed
        self.x_vel = self.speed
        self.y_vel = 0
        self.moving = False
        self.added_speed = added_speed
        self.max_speed = max_speed
        self.__color = color

    def handle_input(self, key):
        if key == pygame.K_SPACE:
            self.moving = True

    def update(self, delta_time):
        movement = pygame.math.Vector2(0.0, 0.0)
        if self.moving:
            movement.x += self.x_vel
            movement.y += self.y_vel        
        self.position += movement * delta_time
                
    def render(self, surface_dest):
        pygame.draw.circle(surface_dest, self.__color, (self.position.x, self.position.y), self.radius)

    def handle_colision(self, left_paddle, right_paddle, screen_size):
        if self.position.y + self.radius >= screen_size[1] or self.position.y - self.radius <= 0:
            self.y_vel *= -1        

        if self.x_vel < 0:            
            if left_paddle.position.y <= self.position.y <= left_paddle.position.y + left_paddle.height:                
                if self.position.x - self.radius <= left_paddle.position.x + left_paddle.width:             
                    self.x_vel *= -1
                    middle_y = left_paddle.position.y + left_paddle.height / 2
                    reduction_factor = (left_paddle.height / 2) / self.speed
                    
                    difference_in_y = middle_y - self.position.y                    
                    y_vel = difference_in_y / reduction_factor
                    self.y_vel = -1 * y_vel 
                    return True                  
        else:            
            if right_paddle.position.y <= self.position.y <= right_paddle.position.y + right_paddle.height:                
                if self.position.x + self.radius >= right_paddle.position.x:                    
                    self.x_vel *= -1
                    middle_y = right_paddle.position.y + right_paddle.height / 2
                    reduction_factor = (right_paddle.height / 2) / self.speed

                    difference_in_y = middle_y - self.position.y                    
                    y_vel = difference_in_y / reduction_factor
                    self.y_vel = -1 * y_vel
                    return True            
        return False

    def reset(self, speed, reset_game):
        self.position = pygame.math.Vector2(self.x, self.y)
        self.y_vel = 0
        if reset_game:
            self.x_vel = -1 * speed
        else: 
            self.x_vel *= -1
        self.moving = False    
                