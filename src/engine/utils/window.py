import pygame as pg
from typing import overload

from src.engine.surface import BaseSurface


class Window(BaseSurface):
    """
    Window.
    """
    
    def __init__(self, width: int, height: int) -> None:
        super().__init__(pg.display.set_mode((width, height)))

    def update(self) -> None:
        """Update window (redrawing)."""
        pg.display.update()
