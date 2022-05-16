class State:
    def __init__(self):
        self.done = False
        self.next_state = ""
        self.previous_state = ""

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_input(self, event):
        pass

    def update(self, delta_time):
        pass

