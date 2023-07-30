from surface.base import BaseSurface, MixinDrawingSurace
from object.base import BaseObject
from utils.directions import RIGHT, LEFT, UP, DOWN
from exception import NonExistDirectionException

MAP_PLAN = [
    '###################',
    '#        #        #',
    '# ## ### # ### ## #',
    '#                 #',
    '# ## # ##### # ## #',
    '#    #   #   #    #',
    '#### ### # ### ####',
    '   # #       # #   ',
    '#### # ## ## # ####',
    '       #   #       ',
    '#### # ##### # ####',
    '   # #       # #   ',
    '#### # ##### # ####',
    '#        #        #',
    '# ## ### # ### ## #',
    '#  #           #  #',
    '## # # ##### # # ##',
    '#    #   #   #    #',
    '# ###### # ###### #',
    '#                 #',
    '###################',
]


EMPTY_BLOCK = ' '
WALL_BLOCK = '#'


class Block:
    __x: int
    __y: int
    __x_real: float
    __y_real: float
    __status: str

    def __init__(self, **kwargs):
        self.__x = kwargs.get("x")
        self.__y = kwargs.get("y")
        self.__x_real = kwargs.get("x_real")
        self.__y_real = kwargs.get("y_real")
        self.__status = kwargs.get("status")

    def is_wall(self) -> bool:
        return self.__status == WALL_BLOCK

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def x_real(self) -> float:
        return self.__x_real

    @property
    def y_real(self) -> float:
        return self.__y_real
    
    def get_distance(self, obj : BaseObject, direction : int) -> float:
        distance = 0
        
        if direction in {RIGHT, LEFT}:
            distance = abs(self.x_real - obj.x)
        elif direction in {DOWN, UP}:
            distance = abs(self.y_real - obj.y)
        else:
            raise NonExistDirectionException
        
        return distance


class BaseMap(BaseSurface):
    __block_width: int
    __block_height: int
    __map: list
    __predrawn_surface: BaseSurface

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__block_width = kwargs.get("block_width")
        self.__block_height = kwargs.get("block_height")
        self.__map = kwargs.get("map_plan")

        self.__predrawn_surface = self.get_predrawn_surface()

    @property
    def map(self) -> list:
        return self.__map

    @property
    def block_width(self) -> int:
        return self.__block_width

    @property
    def block_height(self) -> int:
        return self.__block_height

    def draw(self, surface: MixinDrawingSurace):
        surface.blit(self.__predrawn_surface, (0, 0))

    def get_block(self, x: int, y: int) -> Block:
        status = self.__get_block_status(x=x, y=y)
        x_real, y_real = self.__get_block_coordinates(x, y)
        block = Block(x=x, y=y, x_real=x_real, y_real=y_real)
        return block

    def get_block_by_real_coordinates(self, x_real: float, y_real: float) -> Block:
        x = x_real // self.__block_width
        y = y_real // self.__block_height
        block = self.get_block(x, y)
        return block
    
    
    def get_next_block(self, x : int, y : int, direction : int) -> Block:
        x_add = y_add = 0
        
        if direction == RIGHT:
            x_add = 1
        elif direction == LEFT:
            x_add = -1
        elif direction == DOWN:
            y_add = 1
        elif direction == UP:
            y_add = -1
        else:
            raise NonExistDirectionException
        
        block = self.get_block(x + x_add, y + y_add)
        return block

    def __get_block_coordinates(self, x: int, y: int) -> (float, float):
        x_real = x * self.__block_width + self.__block_width / 2
        y_real = y * self.__block_height + self.__block_height / 2
        return x_real, y_real

    def __get_block_status(self, x: int, y: int) -> str:
        try:
            status = self.__map[y][x]
        except IndexError:
            status = EMPTY_BLOCK

        return status

    def set_object(self, obj: BaseObject, x: int, y: int):
        block = self.get_block(x, y)
        obj.x = block.x_real
        obj.y = block.y_real


class Map(BaseMap):
    __empty_block_color = (0, 0, 0)
    __wall_block_color = (65, 99, 149)

    def __init__(self, x: float, y: float):
        super().__init__(x=x, y=y, width=608, height=608, block_width=34,
                         block_height=34, map_plan=MAP_PLAN)

    def get_predrawn_surface(self) -> BaseSurface:
        predrawn_surface = BaseSurface(
            x=self.x, y=self.y, width=self.width, height=self.height)
        x = y = 0

        for row in self.map:
            x = 0

            for block in row:
                color = self.__empty_block_color if block == EMPTY_BLOCK else self.__wall_block_color
                predrawn_surface.draw_rect(
                    color, (x, y, self.block_width, self.block_height))
                x += self.block_width

            y += self.block_height

        return predrawn_surface
