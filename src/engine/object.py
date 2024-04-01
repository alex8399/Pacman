from abc import ABC
from typing import Tuple


class BaseObject(ABC):
    """
    Abstract base object class.
    """

    __x: float
    __y: float

    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y

    def get_coordinates(self) -> Tuple[float, float]:
        """Get coordinates."""
        return self.__x, self.__y

    def set_coordinates(self, x: float, y: float) -> None:
        """Set coordinates."""
        self.__x = x
        self.__y = y

    def get_x(self) -> float:
        """Get x-coordinate."""
        return self.__x

    def set_x(self, x: float) -> None:
        """Set x-coordinate."""
        self.__x = x

    def get_y(self) -> float:
        """Get y-coordinate."""
        return self.__y

    def set_y(self, y: float) -> None:
        """Set y-coordinate."""
        self.__y = y


class BaseSizeObject(BaseObject, ABC):
    """
    Abstract base object class with sizes.
    """

    __width: float
    __height: float

    def __init__(self, x, y, width, height) -> None:
        super().__init__(x, y)
        self.__width = width
        self.__height = height

    def get_width(self) -> float:
        """Get width."""
        return self.__width

    def set_width(self, width: float) -> None:
        """Set width."""
        self.__width = width

    def get_height(self) -> float:
        """Get height."""
        return self.__height

    def set_height(self, height: float) -> None:
        """Set height."""
        self.__height = height
