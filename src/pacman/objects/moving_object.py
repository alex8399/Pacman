import pygame as pg
from time import sleep
from abc import abstractclassmethod, ABC

from src.engine.exceptions import NonValidSpeedException, NonExistDirectionException, IODeviceException
from src.engine.utils.IOdevices import KeyBoard, Device
from src.engine.object import BaseSizeObject
from src.pacman.surfaces.map import GameMap, BlockStatus
from src.engine.utils.direction import Direction


EPS = 0.2


class MovingObject(BaseSizeObject, ABC):
    """
    Object which moves on the map.
    """

    __direction: int
    __speed: float
    __map: GameMap

    def __init__(self, x: float, y: float, width: float, height: float, speed: float, direction: int, game_map: GameMap):
        super().__init__(x, y, width, height)
        self.__speed = speed
        self.__direction = direction
        self.__map = game_map

    def get_map(self) -> GameMap:
        return self.__map

    def get_speed(self) -> float:
        return self.__speed

    def set_speed(self, speed: float):
        """
        Set speed.

        If speed is negative, NegativeSpeedException is thorwn.
        """

        if speed >= 0:
            self.__speed = speed
        else:
            raise NonValidSpeedException

    def get_direction(self) -> int:
        return self.__direction

    def set_direction(self, direction: int) -> None:
        """
        Set direction.
        
        if non-valid values for direction is received, exception is thrown.
        """
        
        if Direction.is_valid_direction(direction):
            self.__direction = direction
        else:
            raise NonExistDirectionException

    def move(self,) -> None:
        speed = self.get_speed()
        wall_is_met = False

        while speed > EPS and not wall_is_met:
            direction = self.get_direction()
            current_block = self.__map.get_block_by_real_coordinates(self.get_x(), self.get_y())
            distance = current_block.get_distance(self.get_x(), self.get_y(), direction)

            if current_block.is_center_crossed(self.get_x(), self.get_y(), direction):
                next_block = self.__map.get_next_block(current_block, direction)

                if not next_block.is_wall():
                    distance = next_block.get_distance(self.get_x(), self.get_y(), direction=direction)

                    if current_block.is_outside() and next_block.is_outside():
                        teleport_block = self.__map.get_teleport_block(current_block, direction)
                        self.__teleport(teleport_block.get_x(), teleport_block.get_y())
                else:
                    wall_is_met = True

            if not wall_is_met:
                distance = speed if speed < abs(distance) else abs(distance)
                speed -= distance
                self.__move_forward(distance, direction)
                self.__correct_position(current_block.get_x(), current_block.get_y(), direction)


    def __move_forward(self, distance: float, direction: int):
        if direction == Direction.RIGHT:
            self.set_x(self.get_x() + distance)
        elif direction == Direction.LEFT:
            self.set_x(self.get_x() - distance)
        elif direction == Direction.UP:
            self.set_y(self.get_y() - distance)
        elif direction == Direction.DOWN:
            self.set_y(self.get_y() + distance)
        else:
            raise NonExistDirectionException

    def __teleport(self, x: float, y: float):
        self.set_coordinates(x, y)

    def __correct_position(self, block_x: float, block_y: float, direction: int):
        if direction in Direction.X_AXIS:
            self.set_y(block_y)
        elif direction in Direction.Y_AXIS:
            self.set_x(block_x)
        else:
            raise NonExistDirectionException


class KeyboardObject(MovingObject, ABC):
    """
    Object which is driven by keyboard on the map.
    """

    __keyboard_direction: int
    __keyboard: KeyBoard

    def __init__(self, x: float, y: float, width: float, height: float, speed: float,
                 game_map: GameMap, keyboard: KeyBoard, keyboard_direction: int = Direction.RIGHT) -> None:
        super().__init__(x, y, width, height, speed, keyboard_direction, game_map)
        self.__keyboard_direction = keyboard_direction
        self.__keyboard = keyboard

    def get_keyboard_direction(self) -> int:
        return self.__keyboard_direction

    def init_keyboard_direction(self) -> None:
        direction = self.get_keyboard_direction()

        if direction is not None:
            self.__keyboard_direction = direction

    def get_direction(self) -> int:
        game_map = self.get_map()
        current_block = game_map.get_block_by_real_coordinates(self.get_x(), self.get_y())
        next_block = game_map.get_next_block(current_block, self.__keyboard_direction)

        direction = super().get_direction()

        if next_block.is_empty() and current_block.is_center(self.get_x(), self.get_y()):
            self.set_direction(self.__keyboard_direction)
            direction = self.__keyboard_direction

        return direction
    
    def get_keyboard_direction(self) -> int | None:
        """
        Read direction from keyboard.
        if keyboard read no direction, function returns None.

        if errors occurs during the getting keyboard state, IODeviceException is thrown. 
        """

        try:
            keyboard_state = self.__keyboard.get_state()
        except AttributeError:
            raise IODeviceException
        
        direction = None

        if keyboard_state[pg.K_UP]:
            direction = Direction.UP
        elif keyboard_state[pg.K_DOWN]:
            direction = Direction.DOWN
        elif keyboard_state[pg.K_RIGHT]:
            direction = Direction.RIGHT
        elif keyboard_state[pg.K_LEFT]:
            direction = Direction.LEFT

        return direction
    
    def move(self) -> None:
        self.init_keyboard_direction()
        super().move()