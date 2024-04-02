import pygame as pg
from abc import ABC, abstractmethod
from sys import exit

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
    
    __SUCCESS_RETURN_CODE: int = 0

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
        
    def exit(self) -> None:
        """
        Exit from game and stop app.
        """
        exit(self.__SUCCESS_RETURN_CODE)

    def get_window(self) -> Window:
        """
        Get window (the main game surface).
        """
        return self.__window

    def get_clock(self) -> Clock:
        return self.__clock