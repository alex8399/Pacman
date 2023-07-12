import pygame as pg

from object.base import BaseObject


class MixinSurface:
    __body: pg.Surface
    __width : int
    __height : int

    @property
    def body(self) -> pg.Surface:
        return self.__body

    @body.setter
    def body(self, surface: pg.Surface):
        self.__body = surface
        
    @property
    def width(self):
        return self.__body.get_width()
    
    @property
    def height(self) -> int:
        return self.__body.get_height()


class MixinDrawingSurace(MixinSurface):

    def blit(self, surface: 'MixinSurface', *args, **kwargs):
        self.body.blit(surface.body, *args, **kwargs)

    def draw_rect(self, *args, **kwargs):
        pg.draw.rect(self.body, *args, **kwargs)

    def draw_circle(self, *args, **kwargs):
        pg.draw.circle(self.body, *args, **kwargs)


class BaseSurface(MixinDrawingSurace):
    __x: int
    __y: int
    __width: int
    __height: int

    def __init__(self, x: int, y: int, width: int, height: int):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.body = self.__create_surface(width, height)

    @staticmethod
    def __create_surface(width:  int, height: int) -> pg.Surface:
        return pg.Surface((width, height))

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height
