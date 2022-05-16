from importlib import resources
import pygame
from tenis.assets.soundmanager import SoundMannager
from tenis.config import cfg_item
from tenis.entities.paddle import Paddle, PaddleType
from tenis.entities.ball import Ball
from tenis.entities.score import Score

class Game:
    def __init__(self):
        pygame.init()
        
        self.__screen_size = cfg_item("screen_size")
        self.__screen = pygame.display.set_mode(self.__screen_size, 0 , 32)
        with resources.path(*cfg_item("images", "background", "file")) as img_file:
            self.__background_img = pygame.image.load(img_file).convert_alpha()   
        pygame.display.set_caption(cfg_item("game_title"))

        with resources.path(*cfg_item("font", "file")) as font_file:
            self.__font = pygame.font.Font(font_file, cfg_item("font", "size"))

        self.__running = False
        self.__time_per_frame = cfg_item("timing","refresh_stats_time") / cfg_item("timing", "fps")

        self.__paddle_size = cfg_item("entities", "paddle", "size")
        self.__paddle_speed = cfg_item("entities", "paddle", "speed")

        self.__left_paddle = Paddle(10, self.__screen_size[1]//2 - self.__paddle_size[1] //2, self.__paddle_size, self.__paddle_speed, cfg_item("entities", "paddle", "left_color"))
        self.__right_paddle = Paddle(self.__screen_size[0] - 10 - self.__paddle_size[0], self.__screen_size[1] //2 - self.__paddle_size[1]//2, self.__paddle_size, self.__paddle_speed, cfg_item("entities", "paddle", "right_color"))
        self.__ball = Ball(self.__screen_size[0] // 2, self.__screen_size[1] // 2, cfg_item("entities", "ball", "radius"), cfg_item("entities", "ball", "speed"), cfg_item("entities", "ball", "color"))

        self.__left_score = Score(0, self.__font)
        self.__right_score = Score(0, self.__font)

        self.__max_score = cfg_item("entities","score","max")
        self.__winner = None        

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
        elif keys[pygame.K_DOWN] and self.__right_paddle.y + self.__right_paddle.VEL + self.__right_paddle.height <= self.__screen_size[1]:
            self.__right_paddle.update(up=False)
        elif keys[pygame.K_w] and self.__left_paddle.y - self.__left_paddle.VEL >= 0:
            self.__left_paddle.update(up=True)
        elif keys[pygame.K_s] and self.__left_paddle.y + self.__left_paddle.VEL + self.__left_paddle.height <= self.__screen_size[1]:
            self.__left_paddle.update(up=False)         

    def __update(self):
        SoundMannager.instance().play_music("music")
        self.__ball.update()  
        if self.__ball.handle_colision(self.__left_paddle, self.__right_paddle, self.__screen_size):
            SoundMannager.instance().play_sound("shot")
        if self.__ball.x < 0:
            SoundMannager.instance().play_sound("point")            
            self.__right_score.update()
            self.__ball.reset()
        elif self.__ball.x > self.__screen_size[0]:
            SoundMannager.instance().play_sound("point")        
            self.__left_score.update()
            self.__ball.reset()  

        if self.__left_score.score >= self.__max_score:
            self.__left_score.won = True
            self.__winner = self.__left_paddle
            self.__left_paddle.win_text = cfg_item("winning","left")
        elif self.__right_score.score >= self.__max_score:
            self.__right_score.won = True
            self.__winner = self.__right_paddle
            self.__right_paddle.win_text = cfg_item("winning","right")                
        pygame.display.update()
        
    def __render(self):        
        self.__screen.blit(self.__background_img, [0,0])
        self.__ball.render(self.__screen)
        self.__right_paddle.render(self.__screen)
        self.__left_paddle.render(self.__screen)         
        self.__left_score.render(self.__screen, PaddleType.Left, self.__screen_size, self.__left_paddle.color)
        self.__right_score.render(self.__screen, PaddleType.Right, self.__screen_size, self.__right_paddle.color)
        
        if self.__winner:
            self.__final_text = self.__font.render(self.__winner.win_text, 1, self.__winner.color)
            self.__screen.blit(self.__final_text, (self.__screen_size[0]//2 - self.__final_text.get_width() //2, self.__screen_size[1]//2 - self.__final_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(500)
            self.__ball.reset()
            self.__left_paddle.reset()
            self.__left_score.reset()
            self.__right_paddle.reset()
            self.__right_score.reset() 
            self.__winner = None
        
    def __quit(self):
        pygame.quit()

    def __calc_delta_time(self, last):
        current = pygame.time.get_ticks()
        delta = current - last
        return delta, current
