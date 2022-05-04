from typing import List

import pygame

from button import Button
from game import Game
from menu import Menu
from field import Field

# Настройки игры

WINDOW_SIZE = (700, 700)
MENU_SIZE = (WINDOW_SIZE[0], 100)
FIELD_SIZE = (WINDOW_SIZE[0], WINDOW_SIZE[1] - MENU_SIZE[1])
CELLS_COUNT = 2000
GAME_NAME = "Жизнь"
MENU_BUTTON_WIDTH = 200
MENU_COLOR = (255, 255, 255)
MENU_BUTTON_COLOR = (154, 171, 187)
MENU_BUTTON_OPACITY = 100
CELL_ALIVE_COLOR = (0, 255, 0)
CELL_EMPTY_COLOR = (0, 0, 0)


def create_buttons_for_field_menu(field: Field) -> List[Button]:
    buttons = []

    def stop_onclick():
        field.enable()
        for button in buttons:
            if button.action == stop_onclick:
                button.disable()
            else:
                button.enable()

    def start_onclick():
        field.disable()
        for button in buttons:
            if button.action != stop_onclick:
                button.disable()
            else:
                button.enable()

    buttons.append(Button(text="Старт", size=(MENU_BUTTON_WIDTH, 0), action=start_onclick))
    buttons.append(Button(text="Стоп", size=(MENU_BUTTON_WIDTH, 0), action=stop_onclick, enabled=False))
    buttons.append(Button(text="Очистить", size=(MENU_BUTTON_WIDTH, 0), action=field.clean))

    standard_buttons_height = MENU_SIZE[1] / 3
    buttons_inactive_background_color = MENU_BUTTON_COLOR + (MENU_BUTTON_OPACITY,)
    buttons_inactive_text_color = MENU_BUTTON_COLOR + (MENU_BUTTON_OPACITY,)

    for b in buttons:
        b.set_height(standard_buttons_height)
        b.set_background_color(MENU_BUTTON_COLOR)
        b.set_inactive_background_color(buttons_inactive_background_color)
        b.set_inactive_text_color(buttons_inactive_text_color)

    return buttons


if __name__ == "__main__":

    game = Game(window_size=WINDOW_SIZE, game_name=GAME_NAME)
    menu = Menu(size=MENU_SIZE, background_color=MENU_COLOR)
    field = Field(size=FIELD_SIZE, cells_count=CELLS_COUNT, cell_alive_color=CELL_ALIVE_COLOR,
                  cell_empty_color=CELL_EMPTY_COLOR)

    menu.add_buttons(create_buttons_for_field_menu(field))

    game.attach_display_elements([field, menu])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        game.graw()
