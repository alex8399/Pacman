import pygame as pg


class Image:
    __body: pg.surface.Surface

    def __init__(self, image_path: str):
        self.__body = pg.image.load(image_path)

    def get_image(self) -> pg.surface.Surface:
        return self.__body
