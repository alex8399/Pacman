import pygame as pg

from exception import NegativeSpeedException, NonExistDirectionException
from utils.keyboard import KeyBoard

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3


class BaseObject:
    __x: float
    __y: float

    def __init__(self, x: float, y: float):
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


class BaseSizeObject(BaseObject):
    __width: int
    __height: int

    def __init__(self, x: float, y: float, width: int, height: int):
        super().__init__(x, y)
        self.__width = width
        self.__height = height

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, width: int):
        self.__width = width

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, height: int):
        self.__height = height


class MovingObject(BaseSizeObject):
    __direction: int
    __speed: float

    def __init__(self, x: float, y: float, width: int, height: int, speed: float = 0, direction: int = RIGHT):
        super().__init__(x, y, width, height)
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

    def __init__(self, x: float, y: float, width: int, height: int, speed: float = 0, direction: int = RIGHT):
        super().__init__(x, y, width, height, speed, direction)
        self.__manager_direction = direction

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
