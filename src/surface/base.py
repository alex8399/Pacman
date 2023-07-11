import pygame as pg

from object.base import BaseObject


class MixinSurface:
    __body: pg.Surface
    
    def set_body(self, surface : pg.Surface):
        self.__body = surface
    
    def get_body(self) -> pg.Surface:
        return self.__body


class BaseSurface(BaseObject, MixinSurface):

    def __init__(self, surface : 'BaseSurface', x: float, y: float, width: int, height: int):
        super(BaseObject, self).__init__(surface, x, y)
        self.set_body(self.__create_surface(width, height))

    @staticmethod
    def __create_surface(width:  int, height: int) -> pg.Surface:
        return pg.Surface((width, height))