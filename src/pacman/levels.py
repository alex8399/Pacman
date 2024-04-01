import pygame as pg
from typing import overload

from src.engine.utils.clock import Clock
from src.engine.utils.window import Window
from src.engine.game import BaseGame
from src.engine.level import BaseLevel
from src.pacman.objects.pacman import Pacman
from src.pacman.surfaces.map import GameMap


class Level(BaseLevel):
    """
    Level goes according to standart plot of pacman game.
    The main goal of Pacman is to collect all coins and avoid ghosts.
    """

    __map: GameMap
    __pacman: Pacman

    def init_game(self) -> None:
        self.__map = GameMap(x=0, y=0)
        self.__pacman = Pacman(game_map = self.__map, keyboard = self.get_keyboard())
        self.__map.set_object(self.__pacman, 4, 9)
    
    def exec_body(self) -> None:

        for event in self.get_event_handler().get_events():
            if event.get_body().type == pg.QUIT:
                self.exit()

        self.__pacman.move()

    def render(self) -> None:
        self.__map.draw()
        self.__pacman.draw(self.__map)
        self.get_window().draw_surface(self.__map)
