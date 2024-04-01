import pygame as pg

from src.engine.exceptions import NonValidFPSException

class Clock:
    """
    Clock.
    """

    __body: pg.time.Clock
    __fps: int
    
    __DEFAULT_FPS: int = 60
    __MIN_VALUE_FPS: int = 1

    def __init__(self, fps: int = __DEFAULT_FPS) -> None:
        self.__body = self.__create_clock()
        self.set_fps(fps)

    def get_fps(self) -> int:
        return self.__fps

    def set_fps(self, fps: int):
        """
        Set fps.
        
        if fps is less than 1, NonValidFPSException is throw.
        """
        if self.__MIN_VALUE_FPS <= fps:
            self.__fps = fps
        else:
            raise NonValidFPSException

    @staticmethod
    def __create_clock() -> pg.time.Clock:
        return pg.time.Clock()

    def update(self) -> None:
        self.__body.tick(self.__fps)
