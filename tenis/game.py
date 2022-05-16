from importlib import resources
import pygame
from tenis.assets.soundmanager import SoundMannager
from tenis.config import Config, cfg_item
from tenis.states.statemanager import StateManager

class Game:
    def __init__(self):
        pygame.init()
        
        self.__screen_size = cfg_item("screen_size")
        self.__screen = pygame.display.set_mode(self.__screen_size, 0 , 32)
           
        pygame.display.set_caption(cfg_item("game_title"))

        with resources.path(*cfg_item("font", "file")) as font_file:
            self.__font = pygame.font.Font(font_file, cfg_item("font", "size"))

        self.__running = False
        self.__time_per_frame = cfg_item("timing","refresh_stats_time") / cfg_item("timing", "fps")         
        
        self.__state_manager = StateManager()       

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
                self.__update(delta_time)            
            self.__render()
        self.__quit()        

    def __process_events(self):          
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running = False
                if event.key == pygame.K_F5:
                    Config.instance().debug = not Config.instance().debug
            self.__state_manager.handle_input(event)                             

    def __update(self, delta_time):
        self.__state_manager.update(delta_time)        
        
    def __render(self):
        self.__screen.fill(cfg_item("background_color")) 
        self.__state_manager.render(self.__screen)       

    def __quit(self):
        self.__state_manager.quit()
        pygame.quit()

    def __calc_delta_time(self, last):
        current = pygame.time.get_ticks()
        delta = current - last
        return delta, current
