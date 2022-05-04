from typing import List

import pygame
from button import Button

from display_element import DisplayElement


class Menu(DisplayElement):

    def __init__(self, size: tuple, background_color=(0, 0, 0)):
        super().__init__(size=size, background_color=background_color)
        self.__buttons = []

    def draw(self, x, y, display):
        pygame.draw.rect(display, self.background_color, (x, y, self.width, self.height))
        self.__draw_buttons(display, x, y)

    def add_button(self, button: Button):
        self.__buttons.append(button)

    def add_buttons(self, buttons: List[Button]):
        for button in buttons:
            self.add_button(button)

    def __draw_buttons(self, display, x, y):
        padding = (self.width - self.__buttons[0].width * len(self.__buttons)) / (len(self.__buttons) + 1)
        draw_coords = [x + padding, y + padding]

        for button in self.__buttons:
            button.draw(*draw_coords, display)
            draw_coords[0] += button.width + padding
