import pygame as pg
from abc import ABC, abstractmethod

from src.engine.utils.window import Window
from src.engine.utils.clock import Clock
from src.engine.exceptions import ExitException


class BaseGame(ABC):
    """
    Abstract base game class.
    """

    __window: Window
    __clock: Clock
    __label: str

    __DEFAULT_LABEL: str = "MyGame"

    def __init__(self, width: int, height: int, label: str = __DEFAULT_LABEL) -> None:

        pg.init()
        pg.display.set_caption(label)

        self.__window = Window(width, height)
        self.__clock = Clock()
        self.__label = label
        
    @abstractmethod
    def exec(self) -> None:
        """Execute game"""
        pass
        
    @staticmethod
    def exit() -> None:
        """Exit from game and stop app."""
        exit()

    def get_window(self) -> Window:
        """Get window (the main game surface)."""
        return self.__window

    def get_clock(self) -> Clock:
        """Get clock."""
        return self.__clock

    @abstractmethod
    def exec(self) -> None:
        """Execute game"""
        pass
