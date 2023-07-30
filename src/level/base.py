import pygame as pg

from exception import ExitException
from utils.window import Window
from utils.clock import Clock
from utils.eventhandler import Event, EventHandler
from utils.keyboard import KeyBoard
from level.config import LevelBaseConfig


class BaseLevel:
    __config: LevelBaseConfig
    __window: Window
    __clock: Clock
    __event_handler: EventHandler
    __keyboard: KeyBoard

    def __init__(self, window: Window, clock: Clock, config: LevelBaseConfig):
        self.__config = config
        self.__window = window
        self.__clock = clock
        self.__event_handler = EventHandler()
        self.__keyboard = KeyBoard()

    @staticmethod
    def exit():
        raise ExitException

    @property
    def config(self) -> LevelBaseConfig:
        return self.__config

    @property
    def window(self) -> Window:
        return self.__window

    @property
    def clock(self) -> Clock:
        return self.__clock

    @property
    def event_handler(self) -> EventHandler:
        return self.__event_handler

    @property
    def keyboard(self) -> KeyBoard:
        return self.__keyboard

    def update_environment(self):
        self.clock.tick(self.config.ftp)
        self.event_handler.update()
        self.keyboard.update()