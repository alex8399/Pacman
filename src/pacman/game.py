import pygame as pg

from src.engine.exceptions import ExitException
from src.engine.game import BaseGame
from src.pacman.levels import Level


class Game(BaseGame):
    """
    Game.
    """
    
    __WIDTH: int = 580
    __HEIGHT: int = 650
    __LABEL: str = "Pacman"
    
    def __init__(self) -> None:
        super().__init__(self.__WIDTH, self.__HEIGHT, self.__LABEL)

    def exec(self) -> None:
        level = Level(self.get_clock(), self.get_window())
        
        try:
            level.exec()
        except ExitException:
            self.exit()