from surface.base import BaseSurface, MixinDrawingSurace
from object.base import BaseObject
from utils.direction import Direction
from exception import NonExistDirectionException, StatusBlockNonExistException, ObjectMovingException

EPS = 0.1

SCHEME = {
    "map": (
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
    ),
    "empty": ' ',
    "wall": '#',
}


class BlockStatus:
    EMPTY: int = 0
    WALL: int = 1
    OUTSIDE: int = 2


class Block:
    __x: int
    __y: int
    __real_x: float
    __real_y: float
    __status: int

    def __init__(self, **kwargs):
        self.__x = kwargs.get("x")
        self.__y = kwargs.get("y")
        self.__real_x = kwargs.get("real_x")
        self.__real_y = kwargs.get("real_y")
        self.__status = kwargs.get("status")

    def is_wall(self) -> bool:
        return self.__status == BlockStatus.WALL

    def is_empty(self) -> bool:
        return self.__status == BlockStatus.EMPTY

    def is_outside(self) -> bool:
        return self.__status == BlockStatus.OUTSIDE

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def real_x(self) -> float:
        return self.__real_x

    @property
    def real_y(self) -> float:
        return self.__real_y

    def get_distance(self, x: float, y: float, direction: int) -> float:
        distance = 0

        if direction in Direction.X_AXIS:
            distance = self.__real_x - x
        elif direction in Direction.Y_AXIS:
            distance = self.__real_y - y
        else:
            raise NonExistDirectionException

        return distance

    def is_center(self, x: float, y: float) -> bool:
        return abs(x - self.__real_x) < EPS and abs(y - self.__real_y) < EPS

    def is_center_crossed(self, x: float, y: float, direction: int) -> bool:
        reply = True
        distance = self.get_distance(x, y, direction)

        if direction in (Direction.RIGHT, Direction.DOWN):
            if distance > EPS:
                reply = False
        elif direction in (Direction.LEFT, Direction.UP):
            if distance < -EPS:
                reply = False
        else:
            raise NonExistDirectionException

        return reply


class BaseScheme:
    __body: tuple
    __size: tuple

    def __init__(self, scheme: dict):
        scheme, size = self.read_scheme(scheme)

        self.__body = scheme
        self.__size = size

    @property
    def body(self) -> tuple:
        return self.__body

    @property
    def size(self) -> (int, int):
        return self.__size

    def get_status(self, x: int, y: int) -> int:
        size_x, size_y = self.__size

        status = BlockStatus.OUTSIDE
        if 0 <= x < size_x and 0 <= y < size_y:
            status = self.__body[y][x]

        return status


class Scheme(BaseScheme):

    @staticmethod
    def read_scheme(scheme: dict) -> (tuple, (int, int)):
        obj_scheme = tuple()

        for row in scheme["map"]:
            obj_row = tuple()

            for block in row:
                if block == scheme["empty"]:
                    obj_row += (BlockStatus.EMPTY,)
                elif block == scheme["wall"]:
                    obj_row += (BlockStatus.WALL,)
                else:
                    raise StatusBlockNonExistException

            obj_scheme += (obj_row,)

        size = (len(obj_scheme[0]), len(obj_scheme))

        return obj_scheme, size


class BaseMap(BaseSurface):
    __block_width: int
    __block_height: int
    __offset_x: int
    __offset_y: int

    __scheme: BaseScheme
    __predrawn_surface: BaseSurface

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__block_width = kwargs.get("block_width")
        self.__block_height = kwargs.get("block_height")
        self.__offset_x = kwargs.get("offset_x")
        self.__offset_y = kwargs.get("offset_y")

        self.__scheme = Scheme(kwargs.get("scheme"))

        self.__predrawn_surface = self.get_predrawn_surface()

    @property
    def block_width(self) -> int:
        return self.__block_width

    @property
    def block_height(self) -> int:
        return self.__block_height

    @property
    def offset_x(self) -> int:
        return self.__offset_x

    @property
    def offset_y(self) -> int:
        return self.__offset_y

    @property
    def plan(self) -> tuple:
        return self.__scheme.body

    def draw(self, surface: MixinDrawingSurace):
        surface.blit(self.__predrawn_surface, (0, 0))

    def get_block(self, x: int, y: int) -> Block:
        status = self.__scheme.get_status(x, y)
        real_x, real_y = self.__get_block_coordinates(x, y)
        block = Block(x=x, y=y, real_x=real_x, real_y=real_y, status=status)
        return block

    def __get_block_coordinates(self, x: int, y: int) -> (float, float):
        real_x = self.__offset_x + x * self.__block_width + self.__block_width / 2
        real_y = self.__offset_y + y * self.__block_height + self.__block_height / 2
        return real_x, real_y

    def get_block_by_real_coordinates(self, real_x: float, real_y: float) -> Block:
        x = int((real_x - self.__offset_x) // self.__block_width)
        y = int((real_y - self.__offset_y) // self.__block_height)
        block = self.get_block(x, y)
        return block

    def get_next_block(self, current_block: Block, direction: int) -> Block:
        x_add, y_add = Direction.get_adds(direction)
        block = self.get_block(current_block.x + x_add,
                               current_block.y + y_add)
        return block

    def get_teleport_block(self, current_block: Block, direction: int) -> Block:
        block = None
        size_x, size_y = self.__scheme.size

        if direction in Direction.X_AXIS:
            if current_block.x == -1:
                block = self.get_block(size_x, current_block.y)
            elif current_block.x == size_x:
                block = self.get_block(-1, current_block.y)
            else:
                raise ObjectMovingException
        elif direction in Direction.Y_AXIS:
            if current_block.y == -1:
                block = self.get_block(current_block.x, size_y)
            elif current_block.y == size_y:
                block = self.get_block(current_block.x, -1)
            else:
                raise ObjectMovingException
        else:
            raise NonExistDirectionException

        return block

    def set_object(self, obj: BaseObject, x: int, y: int):
        block = self.get_block(x, y)
        obj.x = block.real_x
        obj.y = block.real_y

    def get_predrawn_surface(self) -> BaseSurface:
        return BaseSurface(x=0, y=0, width=self.width, height=self.height)


class Map(BaseMap):
    __empty_block_color = (0, 0, 0)
    __wall_block_color = (65, 99, 149)

    def __init__(self, x: float, y: float):
        super().__init__(x=x, y=y, width=580,
                         height=640, block_width=30,
                         block_height=30, scheme=SCHEME,
                         offset_x=5, offset_y=5)

    def get_predrawn_surface(self) -> BaseSurface:
        predrawn_surface = BaseSurface(
            x=0, y=0, width=self.width, height=self.height)

        y = self.offset_y

        for row in self.plan:
            x = self.offset_x

            for block in row:
                color = self.__empty_block_color if block == BlockStatus.EMPTY else self.__wall_block_color
                predrawn_surface.draw_rect(
                    color, (x, y, self.block_width, self.block_height))
                x += self.block_width

            y += self.block_height

        return predrawn_surface
