import pygame as pg

from surface.base import MixinDrawingSurace


class WindowBaseConfig:
    pass


class WindowConfig(WindowBaseConfig):
    label = "PacMan"
    width = 608
    height = 650


class Window(MixinDrawingSurace):
    __config: WindowBaseConfig

    def __init__(self):
        self.__config = WindowConfig()
        
        pg.init()
        pg.display.set_caption(self.__config.label)
        self.body = self.__create_window(self.__config.width, self.__config.height)

    @staticmethod
    def update():
        pg.display.update()

    @staticmethod
    def __create_window(width: int, height: int) -> pg.Surface:
        return pg.display.set_mode((width, height))
