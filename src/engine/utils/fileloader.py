import pygame as pg
from typing import Type, overload
from abc import ABC, abstractmethod


class BaseFileLoader(ABC):
    """
    Abstract class for loader classes.
    """

    __file: Type
    __path: str

    def __init__(self, file_path: str) -> None:
        __file = self.load_file(file_path)
        __path = file_path

    def get_file(self) -> Type:
        """Get uploaded file."""
        return self.__file

    @abstractmethod
    def load_file(file_path: str):
        """Upload file"""
        pass


class ImageLoader(BaseFileLoader):
    """
    Image loader.
    """

    @overload
    def load_file(self, file_path: str) -> pg.Surface:
        """Upload image."""
        return pg.image.load(file_path)
