class BaseObject:
    __x: float
    __y: float

    def __init__(self, **kwargs):
        self.__x = kwargs.get("x")
        self.__y = kwargs.get("y")

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, x: float):
        self.__x = x

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, y: float):
        self.__y = y


class BaseSizeObject(BaseObject):
    __width: int
    __height: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__width = kwargs.get("width")
        self.__height = kwargs.get("height")

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, width: int):
        self.__width = width

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, height: int):
        self.__height = height