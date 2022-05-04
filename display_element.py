from abc import ABC, abstractmethod


class DisplayElement(ABC):
    def __init__(self, size: tuple, background_color=(0, 0, 0), enabled=True,):
        self.__size = size
        self.__enabled = enabled
        self.__background_color = background_color

    def get_size(self) -> tuple:
        return self.__size

    @property
    def background_color(self) -> tuple:
        return self.__background_color

    def set_background_color(self, color: tuple):
        self.__background_color = color

    @property
    def width(self):
        return self.__size[0]

    def set_width(self, width):
        self.__size = (width, self.height)

    @property
    def height(self):
        return self.__size[1]

    def set_height(self, height):
        self.__size = (self.width, height)

    def is_enabled(self):
        return self.__enabled

    def disable(self):
        self.__enabled = False

    def enable(self):
        self.__enabled = True

    @abstractmethod
    def draw(self, x, y, display):
        pass
