from typing import List, Tuple

import pygame
import pygame.gfxdraw

from display_element import DisplayElement
from math import sqrt


class Field(DisplayElement):
    __AFTER_CELL_CLICK_DELAY = 200
    __AFTER_CHANGE_FIELD_DELAY = 500

    def __init__(self, size: tuple, cells_count: int, cell_alive_color, cell_empty_color):
        super().__init__(size, background_color=(255, 0, 0))
        self.__cells_count = cells_count
        self.__size_of_cell = sqrt(self.width * self.height / cells_count)
        self.__cells_matrix = self.__init_cell_matrix()
        self.__cell_alive_color = cell_alive_color
        self.__cell_empty_color = cell_empty_color

    def draw(self, x, y, display):
        pygame.draw.rect(display, self.background_color, (x, y, *self.get_size()))  # убрать после отладки

        self.__draw_cells(x, y, display)
        if self.is_enabled():
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                mouse_pos = pygame.mouse.get_pos()
                if x < mouse_pos[0] < x + self.width and y < mouse_pos[1] < y + self.height:
                    i, j = self.__get_indexes_by_coords(*mouse_pos, x, y)
                    self.__cells_matrix[i][j] = not self.__cells_matrix[i][j]

                    pygame.time.delay(Field.__AFTER_CELL_CLICK_DELAY)
        else:
            self.__cells_matrix = self.__get_next_cell_matrix()
            pygame.time.delay(Field.__AFTER_CHANGE_FIELD_DELAY)

    def clean(self):
        for i in range(len(self.__cells_matrix)):
            for j in range(len(self.__cells_matrix[i])):
                self.__cells_matrix[i][j] = False

    def __draw_cells(self, x, y, display):
        draw_y = int(y)
        for i in range(len(self.__cells_matrix)):
            draw_x = int(x)
            for j in range(len(self.__cells_matrix[i])):
                draw_color = self.__cell_alive_color if self.__cells_matrix[i][j] else self.__cell_empty_color
                pygame.gfxdraw.box(display, pygame.Rect(draw_x, draw_y, self.__size_of_cell, self.__size_of_cell),
                                   draw_color)
                draw_x += int(self.__size_of_cell)

            draw_y += int(self.__size_of_cell)

    def __get_indexes_by_coords(self, x, y, draw_x, draw_y) -> Tuple[int, int]:
        i = int(y - draw_y) // int(self.__size_of_cell)
        j = int(x - draw_x) // int(self.__size_of_cell)
        return i, j

    def __init_cell_matrix(self) -> List[list]:
        h = int(self.height) // int(self.__size_of_cell) + 1
        w = int(self.width) // int(self.__size_of_cell) + 1

        return [[False for _ in range(w)] for _ in range(h)]

    # Логика игры

    def __get_adjacent_living_cells_count(self, i: int, j: int) -> int:
        left_border = 0
        right_border = len(self.__cells_matrix[0]) - 1
        top_border = 0
        bottom_border = len(self.__cells_matrix) - 1

        def get_checked_indexes(index: int, borders: Tuple[int, int]) -> Tuple[int, int]:
            if index == borders[0]:
                start_index = 0
                end_index = 1
            elif index == borders[1]:
                start_index = -1
                end_index = 0
            else:
                start_index = -1
                end_index = 1

            return start_index, end_index

        start_i, end_i = get_checked_indexes(i, (top_border, bottom_border))
        start_j, end_j = get_checked_indexes(j, (left_border, right_border))

        count = 0
        for adj_i in range(start_i, end_i + 1):
            for adj_j in range(start_j, end_j + 1):
                count += self.__cells_matrix[i + adj_i][j + adj_j]

        count -= self.__cells_matrix[i][j]
        return count

    def __is_alive_cell(self, i: int, j: int) -> bool:
        adjacent_living_cells_count = self.__get_adjacent_living_cells_count(i, j)
        if self.__cells_matrix[i][j]:
            return 1 < adjacent_living_cells_count < 4
        else:
            return adjacent_living_cells_count == 3

    def __get_next_cell_matrix(self) -> List[list]:
        new_cell_matrix = []

        for i in range(len(self.__cells_matrix)):
            new_row = []
            for j in range(len(self.__cells_matrix[i])):
                new_row.append(self.__is_alive_cell(i, j))

            new_cell_matrix.append(new_row)

        return new_cell_matrix
