import pygame as pg

from exception import NegativeSpeedException, NonExistDirectionException, IODeviceException
from utils.IOdevice import KeyBoard, Device
from object.base import BaseSizeObject
from surface.map import BaseMap, BlockStatus
from utils.direction import Direction

from time import sleep

EPS = 0.2


class MovingObject(BaseSizeObject):
    __direction: int
    __speed: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__speed = kwargs.get("speed", 0)
        self.__direction = kwargs.get("direction", Direction.RIGHT)

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

    def move(self, _map: BaseMap):
        if self.is_moving():
            speed = self.get_speed()
            wall_is_met = False

            while speed > EPS and not wall_is_met:
                direction = self.get_direction(_map=_map)
                current_block = _map.get_block_by_real_coordinates(
                    self.x, self.y)
                distance = current_block.get_distance(
                    self.x, self.y, direction)

                if current_block.is_center_crossed(self.x, self.y, direction):
                    next_block = _map.get_next_block(current_block, direction)

                    if not next_block.is_wall():
                        distance = next_block.get_distance(
                            self.x, self.y, direction=direction)

                        if current_block.is_outside() and next_block.is_outside():
                            teleport_block = _map.get_teleport_block(
                                current_block, direction)
                            self.__teleport(teleport_block.real_x,
                                            teleport_block.real_y)
                    else:
                        wall_is_met = True

                if not wall_is_met:
                    distance = speed if speed < abs(
                        distance) else abs(distance)
                    speed -= distance
                    self.__move_forward(distance, direction)
                    self.__correct_position(
                        current_block.real_x, current_block.real_y, direction)

    def is_moving(self, *args, **kwargs) -> bool:
        return True

    def get_direction(self, *args, **kwargs) -> int:
        return self.__direction

    def get_speed(self, *args, **kwargs) -> float:
        return self.__speed

    def __move_forward(self, distance: float, direction: int):
        if direction == Direction.RIGHT:
            self.x += distance
        elif direction == Direction.LEFT:
            self.x -= distance
        elif direction == Direction.UP:
            self.y -= distance
        elif direction == Direction.DOWN:
            self.y += distance
        else:
            raise NonExistDirectionException

    def __teleport(self, x: float, y: float):
        self.x = x
        self.y = y

    def __correct_position(self, block_x: float, block_y: float, direction: int):
        if direction in Direction.X_AXIS:
            self.y = block_y
        elif direction in Direction.Y_AXIS:
            self.x = block_x
        else:
            raise NonExistDirectionException


class ManagingObject(MovingObject):
    __user_direction: int
    __user_device: Device

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__user_direction = kwargs.get("direction", Direction.RIGHT)
        self.__user_device = kwargs.get("user_device")

    @property
    def user_direction(self) -> int:
        return self.__user_direction

    def init_user_direction(self):
        direction = self.get_device_direction(self.__user_device)

        if direction is not None:
            self.__user_direction = direction

    def get_direction(self, _map: BaseMap) -> int:
        current_block = _map.get_block_by_real_coordinates(self.x, self.y)
        next_block = _map.get_next_block(
            current_block, self.__user_direction)

        if next_block.is_empty() and current_block.is_center(self.x, self.y):
            self.direction = self.__user_direction

        direction = self.direction

        return direction


class ManagingKeyboardObject(ManagingObject):

    @staticmethod
    def get_device_direction(keyboard: KeyBoard) -> int | None:
        direction = None

        try:
            if keyboard.is_right_key():
                direction = Direction.RIGHT
            elif keyboard.is_left_key():
                direction = Direction.LEFT
            elif keyboard.is_up_key():
                direction = Direction.UP
            elif keyboard.is_down_key():
                direction = Direction.DOWN
        except AttributeError:
            raise IODeviceException

        return direction
