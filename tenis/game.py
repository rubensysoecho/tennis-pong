from importlib import resources
import pygame
from tenis.config import cfg_item
from tenis.entities.paddle import Paddle
from tenis.entities.ball import Ball

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

        self.__left_score = 0
        self.__right_score = 0

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running = False
                if event.key == pygame.K_UP and self.__right_paddle.y - self.__right_paddle.VEL >= 0:
                    self.__right_paddle.update(up=True)
                elif event.key == pygame.K_DOWN and self.__right_paddle.y + self.__right_paddle.VEL + self.__right_paddle.height <= cfg_item("screen_size")[1]:
                    self.__right_paddle.update(up=False)
                elif event.key == pygame.K_w and self.__left_paddle.y - self.__left_paddle.VEL >= 0:
                    self.__left_paddle.update(up=True)
                elif event.key == pygame.K_s and self.__left_paddle.y + self.__left_paddle.VEL + self.__left_paddle.height <= cfg_item("screen_size")[1]:
                    self.__left_paddle.update(up=False)         

    def __update(self):
        self.__ball.update()        
        
    def __render(self):
        self.__screen.fill(cfg_item("background_color"))
        self.__ball.render(self.__screen)
        self.__right_paddle.render(self.__screen)
        self.__left_paddle.render(self.__screen)        
        pygame.display.update()
        

    def __quit(self):
        pygame.quit()

    def __calc_delta_time(self, last):
        current = pygame.time.get_ticks()
        delta = current - last
        return delta, current
