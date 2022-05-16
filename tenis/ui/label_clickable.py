import pygame
from tenis.ui.label import UILabel

class UILabelClickable(UILabel):

    def __init__(self, center_position, font, text, idle_color, hover_color, bg_color = (0,0,0), action = None):

        super().__init__(center_position, font, text, idle_color, bg_color)

        self._mouse_over = False
        self._hover_image = font.render(text, True, hover_color, bg_color)
        self.action = action

    def handle_input(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self._mouse_over = True
            else:
                self._mouse_over = False

        if event.type == pygame.MOUSEBUTTONUP:
            if self._mouse_over and event.button == 1:
                return self.action

        return None

    def render(self, surface):
        image = self._hover_image if self._mouse_over else self._image
        surface.blit(image, self.rect)
