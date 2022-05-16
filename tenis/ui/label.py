class UILabel:

    def __init__(self, center_position, font, text, idle_color, bg_color = (0,0,0)):
        self._image = font.render(text, True, idle_color, bg_color)
        self.rect = self._image.get_rect(center = center_position)

    def handle_input(self, event):
        pass

    def update(self, delta_time):
        pass

    def render(self, surface):
        surface.blit(self._image, self.rect)
        