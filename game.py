from typing import List

import pygame
from display_element import DisplayElement


class Game:
    __instance = None

    def __init__(self, window_size: tuple, game_name: str):
        if Game.__instance is None:
            pygame.init()
            self.__window_size = window_size
            self.__display = pygame.display.set_mode(window_size)
            pygame.display.set_caption(game_name)
            self.__display_elements = []

            Game.__instance = self
        else:
            self.get_instance()

    @classmethod
    def get_instance(cls):
        return Game.__instance

    def attach_display_element(self, element: DisplayElement):
        self.__display_elements.append(element)

    def attach_display_elements(self, elements: List[DisplayElement]):
        for element in elements:
            self.attach_display_element(element)

    def get_window_size(self):
        return self.__window_size

    def graw(self):
        draw_coord_x = 0
        draw_coord_y = 0

        for element in self.__display_elements:
            element.draw(draw_coord_x, draw_coord_y, self.__display)
            draw_coord_y += element.height

        pygame.display.flip()
