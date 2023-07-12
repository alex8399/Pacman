import pygame as pg

from surface.base import MixinSurface


class Image(MixinSurface):
    __path: str

    def __init__(self, image_path: str):
        self.__path = image_path
        self.body = self.__load_image(image_path)

    @staticmethod
    def __load_image(image_path: str) -> pg.Surface:
        return pg.image.load(image_path)

    @property
    def path(self) -> str:
        return self.__path
