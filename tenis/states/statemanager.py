from tenis.states.gameplay import GamePlay
from tenis.states.intro import Intro

class StateManager:

    def __init__(self):
        self.__states = {
            "Intro" : Intro(),
            "GamePlay" : GamePlay()
        }

        self.__current_state_name = "Intro"
        self.__current_state = self.__states[self.__current_state_name]
        self.__current_state.enter()

    def handle_input(self, event):
        self.__current_state.handle_input(event)
    
    def __quit(self):
        pass


    def update(self, delta_time):
        if self.__current_state.done:
            self.__change_state()
        self.__current_state.update(delta_time)

    def render(self, surface):
        self.__current_state.render(surface)

    def quit(self):
        self.__current_state.exit()

    def __change_state(self):
        self.__current_state.exit()

        previous_state = self.__current_state_name
        self.__current_state_name  = self.__current_state.next_state
        self.__current_state = self.__states[self.__current_state_name]
        self.__current_state.previous_state = previous_state
        self.__current_state.enter()
        