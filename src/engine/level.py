import pygame as pg
from abc import ABC, abstractmethod

from src.engine.exceptions import ExitException
from src.engine.utils.window import Window
from src.engine.utils.clock import Clock
from src.engine.utils.IOdevices import KeyBoard
from src.engine.utils.eventhandler import EventHandler


class BaseLevel(ABC):
    """
    Abstract base level class.
    """
    
    __window: Window
    __clock: Clock

    __event_handler: EventHandler
    __keyboard: KeyBoard

    __run: bool

    def __init__(self, game) -> None:
        self.__clock = game.get_clock()
        self.__window = game.get_window()

        self.__event_handler = EventHandler()
        self.__keyboard = KeyBoard()

        self.__run = True

    def exec(self) -> None:
        """Execute level."""
        self.init_game()

        while self.__run:
            self.pre_update_environment()
            self.exec_body()
            self.render()
            self.post_update_environment()

    @abstractmethod
    def init_game(self) -> None:
        """Init environment of game."""
        pass

    def pre_update_environment(self) -> None:
        """Update enviroment before executing main body:
            - ticking clock,
            - uploading new events in event handler,
            - updating state of keyboard."""

        self.__clock.update()
        self.__event_handler.update()
        self.__keyboard.update()

    @abstractmethod
    def exec_body(self) -> None:
        "Execute game body."
        pass


    def render(self) -> None:
        "Render level objects."
        pass

    def post_update_environment(self) -> None:
        """Update environment after executin main body:
            - redrawing window."""
        self.__window.update()
    
    def get_clock(self) -> Clock:
        return self.__clock

    def get_window(self) -> Window:
        return self.__window

    def get_event_handler(self) -> EventHandler:
        return self.__event_handler

    def get_keyboard(self) -> KeyBoard:
        return self.__keyboard

    @staticmethod
    def exit() -> None:
        raise ExitException

    def stop(self):
        self.__run = False

    def is_running(self) -> bool:
        return self.__run
