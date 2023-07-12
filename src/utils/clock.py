import pygame as pg


class Clock:
    __body: pg.time.Clock

    def __init__(self):
        self.__body = self.__create_clock()

    @staticmethod
    def __create_clock() -> pg.time.Clock:
        return pg.time.Clock()

    def tick(self, ftp: int):
        self.__body.tick(ftp)
