from importlib import resources
import pygame
from tenis.config import cfg_item
from tenis.entities.paddle import Paddle
from tenis.entities.ball import Ball
from tenis.entities.score import Score

class Game:
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode(cfg_item("screen_size"), 0, 32)
        pygame.display.set_caption(cfg_item("game_title"))

        with resources.path(*cfg_item("font", "file")) as font_file:
            self.__font = pygame.font.Font(font_file, cfg_item("font", "size"))

        self.__running = False
        self.__time_per_frame = 1000.0/cfg_item("timing", "fps")

        self.__left_paddle = Paddle(10, cfg_item("screen_size")[1]//2 - cfg_item("paddle_size")[1] //2, cfg_item("paddle_size")[0], cfg_item("paddle_size")[1])
        self.__right_paddle = Paddle(cfg_item("screen_size")[0] - 10 - cfg_item("paddle_size")[0], cfg_item("screen_size")[1] //2 - cfg_item("paddle_size")[1]//2, cfg_item("paddle_size")[0], cfg_item("paddle_size")[1])
        self.__ball = Ball(cfg_item("screen_size")[0] // 2, cfg_item("screen_size")[1] // 2, cfg_item("ball_radius"))

        self.__left_score = Score(0)
        self.__right_score = Score(0)

        self.__won = False
        self.__win_text = ""

    def run(self):
        self.__running = True
        last_time = pygame.time.get_ticks()
        time_since_last_update = 0

        while self.__running:
            delta_time, last_time = self.__calc_delta_time(last_time)
            time_since_last_update += delta_time
            while time_since_last_update > self.__time_per_frame:
                time_since_last_update -= self.__time_per_frame
                self.__process_events()
                self.__update()

            self.__render()

        self.__quit()        

    def __process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False   
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.__right_paddle.y - self.__right_paddle.VEL >= 0:
            self.__right_paddle.update(up=True)
        elif keys[pygame.K_DOWN] and self.__right_paddle.y + self.__right_paddle.VEL + self.__right_paddle.height <= cfg_item("screen_size")[1]:
            self.__right_paddle.update(up=False)
        elif keys[pygame.K_w] and self.__left_paddle.y - self.__left_paddle.VEL >= 0:
            self.__left_paddle.update(up=True)
        elif keys[pygame.K_s] and self.__left_paddle.y + self.__left_paddle.VEL + self.__left_paddle.height <= cfg_item("screen_size")[1]:
            self.__left_paddle.update(up=False)         

    def __update(self):
        self.__ball.update()  
        if self.__ball.x < 0:
            self.__right_score.update()
            self.__ball.reset()
        elif self.__ball.x > cfg_item("screen_size")[0]:
            self.__left_score.update()
            self.__ball.reset()  

        if self.__left_score.score >= cfg_item("winning_score"):
            self.__won = True
            self.__win_text = cfg_item("won_left")
        elif self.__right_score.score >= cfg_item("winning_score"):
            self.__won = True
            self.__win_text = cfg_item("won_right")                
        pygame.display.update()
        
    def __render(self):
        self.__screen.fill(cfg_item("background_color"))
        self.__ball.render(self.__screen)
        self.__right_paddle.render(self.__screen)
        self.__left_paddle.render(self.__screen)         
        self.__screen.blit(self.__left_score.render(), (cfg_item("screen_size")[0]//4-self.__left_score.render().get_width()//2, 20))
        self.__screen.blit(self.__right_score.render(), (cfg_item("screen_size")[0]*(3/4)-self.__right_score.render().get_width()//2, 20))        
        
        if self.__won:
            self.__final_text = self.__font.render(self.__win_text, 1, cfg_item("object_color"))
            self.__screen.blit(self.__final_text, (cfg_item("screen_size")[0]//2 - self.__final_text.get_width() //2, cfg_item("screen_size")[1]//2 - self.__final_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(1000)
            self.__ball.reset()
            self.__left_paddle.reset()
            self.__left_score.reset()
            self.__right_paddle.reset()
            self.__right_score.reset() 
            self.__won = False
        
    def __quit(self):
        pygame.quit()

    def __calc_delta_time(self, last):
        current = pygame.time.get_ticks()
        delta = current - last
        return delta, current
