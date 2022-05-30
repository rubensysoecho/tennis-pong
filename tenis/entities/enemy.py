from tenis.entities.paddle import Paddle

class Enemy(Paddle):
    def __init__(self, x, y, size, speed, color, added_height):
        super().__init__(x, y, size, speed, color)
        self.added_height = added_height

    def check_bounds(self, screen_size):
        self.moving_down = True
        if self.position.y <= 0:            
            self.moving_up = False
            self.moving_down = True
        elif self.position.y >= screen_size[1] - self.height:
            self.moving_up = True
            self.moving_down = True

    def handle_colision(self, ball, screen_size):
        if ball.moving:
            if self.position.y <= ball.position.y <= self.position.y + self.height:
                if self.position.x <= ball.position.x - ball.radius <= self.position.x + self.width:                                    
                    if abs(ball.x_vel) <= ball.max_speed:
                        if ball.x_vel < 0:
                            ball.x_vel -= ball.added_speed
                        else:
                            ball.x_vel += ball.added_speed                                            
                    if self.height < screen_size[1] // 3:
                        self.height += self.added_height                               
                    ball.x_vel *= -1 
                    return True
        return False

                        


