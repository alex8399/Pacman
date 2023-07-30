import pygame as pg

from exception import NegativeSpeedException, NonExistDirectionException
from utils.keyboard import KeyBoard
from object.base import BaseSizeObject
from surface.map import BaseMap, EMPTY_BLOCK, WALL_BLOCK
from utils.directions import RIGHT, LEFT, UP, DOWN


class MovingObject(BaseSizeObject):
    __direction: int
    __speed: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__speed = kwargs.get("speed", 0)
        self.__direction = kwargs.get("direction", RIGHT)

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

    def move(self, map: BaseMap):
        speed = self.get_speed()
        wall_is_met = False
        
        while speed > 0 and not wall_is_met:
            direction = self.get_direction()
            current_block = map.get_block_by_real_coordinates(self.x, self.y)
            
            if current_block.is_center_crossed(self):
                next_block = map.get_next_block(current_block.x, current_block.y, direction)
                distance = next_block.get_distance(self, direction)
                
                if next_block.is_wall():
                    wall_is_met = True
            else:
                distance = current_block.get_distance(self, direction)
            
            if not wall_is_met:
                distance = speed if speed < distance else distance
                self.__move_forward(distance, direction)
                speed -= distance
                
    
    
    def __move_forward(self, distance : float, direction : int):
        if direction == RIGHT:
            self.x += distance
        elif direction == LEFT:
            self.x -= distance
        elif direction == UP:
            self.y -= distance
        elif direction == DOWN:
            self.y += distance
        else:
            raise NonExistDirectionException
    
    def get_direction(self) -> int:
        return self.__direction
    
    def get_speed(self) -> float:
        return self.__speed

class ManagingObject(MovingObject):
    __user_direction: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__user_direction = kwargs.get('direction', RIGHT)

    def init_user_direction(self, keyboard: KeyBoard):
        direction = self.__get_keyborad_direction(keyboard)

        if direction is not None:
            self.__user_direction = direction
    
    def get_direction(self) -> int:
        return self.__user_direction

    @property
    def user_direction(self) -> int:
        return self.__user_direction

    @staticmethod
    def __get_keyborad_direction(keyboard: KeyBoard) -> int | None:
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
