import pygame as pg


class KeyBoard:
    __keys: list

    def __init__(self):
        self.__keys = list()

    def update(self):
        self.__keys = self.__init_keys()

    @staticmethod
    def __init_keys() -> list:
        return pg.keys.get_pressed()

    def is_right_key(self) -> bool:
        return self.__keys[pg.K_RIGHT]

    def is_left_key(self) -> bool:
        return self.__keys[pg.K_LEFT]

    def is_up_key(self) -> bool:
        return self.__keys[pg.K_UP]

    def is_down_key(self) -> bool:
        return self.__keys[pg.K_DOWN]
