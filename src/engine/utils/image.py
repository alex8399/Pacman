import pygame as pg
from typing import overload

from src.engine.surface import BaseSurface
from src.engine.utils.fileloader import ImageLoader

class Image(BaseSurface):
    """
    Image.
    """
    
    @overload
    def __init__(self, image_path: str) -> None:
        super().__init__(ImageLoader(image_path).get_file())