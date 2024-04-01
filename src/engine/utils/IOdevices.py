import pygame as pg
from abc import ABC
from typing import List


class Device(ABC):
    """
    Abstract device class.
    """
    pass


class KeyBoard(Device):
    """
    Keyboard.
    """

    __keys: List[bool]

    def __init__(self) -> None:
        self.__keys = list()

    def get_state(self) -> List[bool]:
        """
        Get keyboard state (pressed keys).
        """
        return self.__keys

    def update(self) -> None:
        """
        Update keyboard state (receive new array of keys' statuses).
        """
        self.__keys = pg.key.get_pressed()
