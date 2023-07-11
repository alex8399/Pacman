import pygame as pg

from exception import NegativeSpeedException, NonExistDirectionException
from utils.keyboard import KeyBoard
from surface.base import BaseSurface

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3


class BaseObject:
    __surface: BaseSurface
    __x: float
    __y: float

    def __init__(self, surface: BaseSurface, x: float, y: float):
        self.__surface = surface
        self.__x = x
        self.__y = y

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, x: float):
        self.__x = x

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, y: float):
        self.__y = y

    def get_surface(self) -> BaseSurface:
        return self.__surface


class MovingObject(BaseObject):
    __direction: int
    __speed: float

    def __init__(self, surface: BaseSurface, x: float, y: float, speed: float = 0, direction: int = RIGHT):
        super().__init__(surface, x, y)
        self.__speed = speed
        self.__direction = direction

    @property
    def speed(self) -> float:
        return self.__speed

    @speed.setter
    def speed(self, speed: float):
        if speed >= 0:
            self.__speed = speed
        else:
            raise NegativeSpeedException

    @property
    def direction(self) -> int:
        return self.__direction

    @direction.setter
    def direction(self, direction: int):
        if 0 <= direction <= 3:
            self.__direction = direction
        else:
            raise NonExistDirectionException


class ManagingObject(MovingObject):
    __manager_direction: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__manager_direction = self.direction

    def init_direction_from_manager(self, keyboard: KeyBoard):
        direction = self.__get_direction_from_keyboard(keyboard)

        if direction is not None:
            self.__manager_direction = direction

    @staticmethod
    def __get_direction_from_keyboard(keyboard: KeyBoard) -> int | None:
        direction = None

        if keyboard.is_right_key():
            direction = RIGHT
        elif keyboard.is_left_key():
            direction = LEFT
        elif keyboard.is_up_key():
            direction = UP
        elif keyboard.is_down_key():
            direction = DOWN

        return direction
