from importlib import resources
from enum import Enum
import pygame
from tenis.config import cfg_item
from tenis.states.state import State
from tenis.ui.label import UILabel
from tenis.ui.label_clickable import UILabelClickable

class Actions(Enum):
    Next_Level = 0

class Intro(State):

    def __init__(self):
        super().__init__()
        self.next_state = "GamePlay"

        with resources.path(*cfg_item("font", "file")) as font_file:
            self.__font = pygame.font.Font(font_file, cfg_item("font", "intro_size"))

        self.__button = UILabelClickable(cfg_item('states','intro','button','position'), self.__font, cfg_item('states','intro','button','text'), cfg_item('states','intro','button','color'), cfg_item('states','intro','button','hover_color'), action = Actions.Next_Level)

        self.__label = UILabel(cfg_item('states','intro','label','position'), self.__font, cfg_item('states','intro','label','text'), cfg_item('states','intro','label','color'))

    def enter(self):
        self.done = False

    def exit(self):
        pass

    def handle_input(self, event):
        if self.__button.handle_input(event) == Actions.Next_Level:
            self.done = True

    def update(self, delta_time):
        pass

    def render(self, surface):
        self.__button.render(surface)
        self.__label.render(surface)