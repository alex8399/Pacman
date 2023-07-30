import pygame as pg
from sys import exit as exit

from utils.window import Window
from exception import ExitException
from utils.clock import Clock
from level.base import BaseLevel
from level.level_01 import Level01


class BaseGame:
    __window: Window
    __clock: Clock

    def __init__(self):
        self.__window = Window()
        self.__clock = Clock()

    @staticmethod
    def exit():
        exit()

    @property
    def window(self) -> Window:
        return self.__window

    @property
    def clock(self) -> Clock:
        return self.__clock


class Game(BaseGame):

    def exec(self):
        level = Level01(self.window, self.clock)

        try:
            level.exec()
        except ExitException:
            self.exit()


def play_game():
    game = Game()
    game.exec()