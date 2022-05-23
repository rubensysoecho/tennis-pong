import pygame
from importlib import resources
from tenis.config import cfg_item
from tenis.entities.paddle import PaddleType
from tenis.entities.ball import Ball
from tenis.entities.player import Player
from tenis.entities.score import Score
from tenis.entities.enemy import Enemy
from tenis.states.state import State
from tenis.assets.soundmanager import SoundMannager

class GamePlay(State):
    def __init__(self):
        super().__init__()
        self.next_state = "Intro"

        self.__screen_size = cfg_item("screen_size")
        with resources.path(*cfg_item("images", "background", "file")) as img_file:
            self.__background_img = pygame.image.load(img_file).convert_alpha()
        with resources.path(*cfg_item("font", "file")) as font_file:
            self.__font = pygame.font.Font(font_file, cfg_item("font", "size"))
        
        self.__paddle_size = cfg_item("entities", "paddle", "size")
        self.__player_speed = cfg_item("entities", "paddle", "player", "speed")
        
        self.__left_paddle = Player(10, self.__screen_size[1]//2 - self.__paddle_size[1] //2, self.__paddle_size, self.__player_speed, cfg_item("entities", "paddle", "player", "left_color"))
        self.__right_paddle = Player(self.__screen_size[0] - 10 - self.__paddle_size[0], self.__screen_size[1] //2 - self.__paddle_size[1]//2, self.__paddle_size, self.__player_speed, cfg_item("entities", "paddle", "player", "right_color"))
        self.__ball = Ball(self.__screen_size[0] // 2, self.__screen_size[1] // 2, cfg_item("entities", "ball", "radius"), cfg_item("entities", "ball", "speed"), cfg_item("entities", "ball", "added_speed"), cfg_item("entities", "ball", "max_speed"), cfg_item("entities", "ball", "color"))
        self.__enemy = Enemy((self.__screen_size[0] // 2) - self.__paddle_size[0] // 2, self.__screen_size[1] // 2, self.__paddle_size, cfg_item("entities", "paddle", "enemy", "speed"), cfg_item("entities", "paddle", "enemy", "color"), cfg_item("entities", "paddle", "enemy", "added_height"))
        
        self.__left_score = Score(0, cfg_item("entities", "score", "left_position"), self.__font)
        self.__right_score = Score(0, cfg_item("entities", "score", "right_position"), self.__font)
        
        self.__max_score = cfg_item("entities","score","max")
        self.__winner = None

    def enter(self):
        self.done = False
        self.__start()

    def exit(self):
        self.__quit()

    def handle_input(self, event):   
        if event.type == pygame.KEYUP:
            self.__input(event.key, False)
        if event.type == pygame.KEYDOWN:
            self.__input(event.key, True)        
        
    def __input(self, key, is_pressed):        
        if key == pygame.K_UP:            
            self.__right_paddle.moving_up=is_pressed
        elif key == pygame.K_DOWN:
            self.__right_paddle.moving_down=is_pressed
        elif key == pygame.K_w:
            self.__left_paddle.moving_up=is_pressed
        elif key == pygame.K_s:
            self.__left_paddle.moving_down=is_pressed
        elif key == pygame.K_SPACE:
            self.__ball.handle_input(key)

    def update(self, delta_time):        
        self.__ball.update(delta_time)          
        self.__right_paddle.update(delta_time, self.__screen_size)
        self.__left_paddle.update(delta_time, self.__screen_size)
        self.__enemy.update(delta_time, self.__screen_size)
        if self.__ball.handle_colision(self.__left_paddle, self.__right_paddle, self.__screen_size):                
            SoundMannager.instance().play_sound(cfg_item("sfx", "shot", "audio_file")) 
        if  self.__enemy.handle_colision(self.__ball, self.__screen_size):                          
            SoundMannager.instance().play_sound(cfg_item("sfx", "error", "audio_file")) 
        if self.__ball.position.x < 0:            
            SoundMannager.instance().play_sound(cfg_item("sfx", "point", "audio_file"))            
            self.__right_score.update()
            self.__ball.reset(cfg_item("entities", "ball", "speed"), False)
        elif self.__ball.position.x > self.__screen_size[0]:
            SoundMannager.instance().play_sound(cfg_item("sfx", "point", "audio_file"))        
            self.__left_score.update()
            self.__ball.reset(cfg_item("entities", "ball", "speed"), False)  

        if self.__left_score.score >= self.__max_score:
            self.__left_score.won = True
            self.__winner = self.__left_paddle
            self.__left_paddle.win_text = cfg_item("winning","left")
            self.game_over()
        elif self.__right_score.score >= self.__max_score:
            self.__right_score.won = True
            self.__winner = self.__right_paddle
            self.__right_paddle.win_text = cfg_item("winning","right")                
            self.game_over()        

    def render(self, screen):    
        screen.blit(self.__background_img, [0,0])        
        self.__ball.render(screen)
        self.__right_paddle.render(screen)
        self.__left_paddle.render(screen)
        self.__enemy.render(screen)         
        self.__left_score.render(screen, PaddleType.Left, self.__screen_size, self.__left_paddle.color)
        self.__right_score.render(screen, PaddleType.Right, self.__screen_size, self.__right_paddle.color)        
        if self.__winner:
            self.__reset(screen)        

    def __start(self):
        SoundMannager.instance().play_music(cfg_item("music", "music", "audio_file"))        

    def exit(self):
        pass

    def game_over(self):
        self.done = True
        SoundMannager.instance().stop_music(cfg_item('states', 'game_over_time'))

    def __reset(self, screen):        
        self.__final_text = self.__font.render(self.__winner.win_text, 1, self.__winner.color)
        screen.blit(self.__final_text, (self.__screen_size[0]//2 - self.__final_text.get_width() //2, self.__screen_size[1]//2 - self.__final_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(500)
        self.__ball.reset(cfg_item("entities", "ball", "speed"), True)
        self.__left_paddle.reset(self.__paddle_size)
        self.__left_score.reset()
        self.__right_paddle.reset(self.__paddle_size)
        self.__right_score.reset() 
        self.__enemy.reset(self.__paddle_size)
        self.__winner = None
    