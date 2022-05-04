import pygame
import pygame.gfxdraw
from display_element import DisplayElement


class Button(DisplayElement):

    def __init__(self, size: tuple,
                 background_color=(0, 0, 0), enabled=True, inactive_background_color=None,
                 text_color=(0, 0, 0), inactive_text_color=None, text="",
                 action=None,
                 after_click_delay: int = 300):

        super().__init__(size, background_color, enabled)
        self.__inactive_background_color = inactive_background_color
        self.__inactive_text_color = inactive_text_color
        self.__text_color = text_color
        self.__text = text
        self.__after_click_delay = after_click_delay
        self.__action = action

    # Геттеры

    @property
    def text_color(self) -> tuple:
        return self.__text_color

    @property
    def inactive_text_color(self) -> tuple:
        if self.__inactive_text_color is None:
            return self.text_color
        else:
            return self.__inactive_text_color

    @property
    def inactive_background_color(self):
        if self.__inactive_background_color is None:
            return self.background_color
        else:
            return self.__inactive_background_color

    @property
    def action(self):
        return self.__action

    # Сеттеры

    def set_text(self, text: str):
        self.__text = text

    def set_onclick_action(self, action):
        self.__action = action

    def set_text_color(self, color: tuple):
        self.__text_color = color

    def set_inactive_text_color(self, color: tuple):
        self.__inactive_text_color = color

    def set_inactive_background_color(self, color: tuple):
        self.__inactive_background_color = color

    def draw(self, x, y, display):
        if self.is_enabled():
            draw_color = self.background_color
        else:
            draw_color = self.inactive_background_color

        pygame.gfxdraw.box(display, pygame.Rect(x, y, self.width, self.height), draw_color)

        self.__draw_text(display, x, y)
        self.__catch_onclick_action(x, y)

    def __catch_onclick_action(self, x, y):
        if self.is_enabled():
            click = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            # Условие попадания курсором по кнопке
            if x < mouse_pos[0] < x + self.width and y < mouse_pos[1] < y + self.height:
                if click[0] == 1:
                    if self.__action is not None:
                        self.__action()
                        pygame.time.delay(self.__after_click_delay)

    def __draw_text(self, display, x, y):
        if self.is_enabled():
            draw_color = self.text_color
        else:
            draw_color = self.inactive_text_color

        button_font = pygame.font.Font(None, 30)
        button_text = button_font.render(self.__text, False, draw_color)

        # Альфа-канал цвета указан
        if len(draw_color) == 4:
            button_text.set_alpha(draw_color[3])

        text_size = button_font.size(self.__text)
        text_position_x = x + self.width / 2 - text_size[0] / 2
        text_position_y = y + self.height / 2 - text_size[1] / 2

        display.blit(button_text, (text_position_x, text_position_y))
