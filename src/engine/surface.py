import pygame as pg
from typing import overload, Tuple
from abc import ABC

from src.engine.object import BaseObject

class BaseSurface(ABC):
    """
    Abstract base surface class.
    """
    
    __body: pg.Surface
    
    def __init__(self, surface: pg.Surface) -> None:
        self.__body = surface

    def get_surface(self) -> pg.Surface:
        return self.__body
        
    def get_width(self) -> int:
        return self.__body.get_width()
    
    def get_height(self) -> int:
        return self.__body.get_height()
    
    def draw_surface(self, surface: 'BaseCoordinateSurface') -> None:
        coordinates = (int(surface.get_x()), int(surface.get_y()))
        self.__body.blit(surface.get_surface(), coordinates)

    def draw_rect(self, *args, **kwargs) -> None:
        pg.draw.rect(self.__body, *args, **kwargs)
        
    def draw_circle(self, *args, **kwargs) -> None:
        pg.draw.circle(self.__body, *args, **kwargs)
    
    
class BaseCoordinateSurface(BaseSurface, BaseObject, ABC):
    """
    Abstract base surface class with coordinates.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__(pg.Surface((width, height)))
        self.set_coordinates(x, y)
