import pygame as pg

from surface.base import MixinSurface


class WindowBaseConfig:
    pass


class WindowConfig(WindowBaseConfig):
    label = "PacMan"
    width = 700
    height = 700


class Window(MixinSurface):
    __config: WindowBaseConfig

    def __init__(self):
        self.__config = WindowConfig()

        pg.init()
        pg.display.set_caption(self.__config.label)
        self.set_body(self.self.__create_window(self.__config.width, self.__config.height))

    def update(self):
        pg.display.update()

    @staticmethod
    def __create_window(width: int, height: int) -> pg.Surface:
        return pg.display.set_mode((width, height))
