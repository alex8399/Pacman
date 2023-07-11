import pygame as pg

from surface.map import TestMap
from exception import ExitException
from utils.window import Window
from utils.clock import Clock
from utils.event_handler import Event, EventHandler
from utils.keyboard import KeyBoard

from object.pacman import Pacman


class LevelBaseConfig:
    pass


class LevelConfig(LevelBaseConfig):
    ftp: int = 60


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
    
    def draw(self):
        self.window.update()

class Level01(BaseLevel):

    def __init__(self, window : Window, clock : Clock):
        super().__init__(window, clock, LevelConfig())

    def draw(self):
        super().draw()
        
    def exec(self):
        run = True
        
        while run:
            self.update_environment()

            for event in self.event_handler.get_events():
                if event.is_exit():
                    self.exit()
            
            print(1)

            self.draw()
