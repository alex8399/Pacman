from typing import Tuple, Dict

from src.engine.surface import BaseCoordinateSurface, BaseSurface
from src.engine.surface import BaseObject
from src.engine.utils.direction import Direction
from src.engine.exceptions import NonExistDirectionException, StatusBlockNonExistException, ObjectMovingException

EPS = 0.1


class BlockStatus:
    EMPTY: int = 0
    WALL: int = 1
    OUTSIDE: int = 2


class Block(BaseObject):
    __map_x: int
    __map_y: int
    __status: int

    def __init__(self, x, y, map_x, map_y, status):
        super().__init__(x, y)
        self.__map_x = map_x
        self.__map_y = map_y
        self.__status = status

    def is_wall(self) -> bool:
        return self.__status == BlockStatus.WALL

    def is_empty(self) -> bool:
        return self.__status == BlockStatus.EMPTY

    def is_outside(self) -> bool:
        return self.__status == BlockStatus.OUTSIDE

    def get_map_x(self) -> int:
        return self.__map_x

    def get_map_y(self) -> int:
        return self.__map_y

    def get_distance(self, x: float, y: float, direction: int) -> float:
        distance = 0

        if direction in Direction.X_AXIS:
            distance = self.get_x() - x
        elif direction in Direction.Y_AXIS:
            distance = self.get_y() - y
        else:
            raise NonExistDirectionException

        return distance

    def is_center(self, x: float, y: float) -> bool:
        return abs(x - self.get_x()) < EPS and abs(y - self.get_y()) < EPS

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


class Scheme:
    __body: Tuple

    def __init__(self, scheme: dict):
        self.__body = self.read_scheme(scheme)

    def get_plan(self) -> tuple:
        return self.__body

    def get_size(self) -> Tuple[int, int]:
        return(len(self.__body[0]), len(self.__body))
        

    def get_status(self, x: int, y: int) -> int:
        size_x, size_y = self.get_size()

        status = BlockStatus.OUTSIDE

        try:
            if 0 <= x < size_x and 0 <= y < size_y:
                status = self.__body[y][x]
        except IndexError:
            status = BlockStatus.OUTSIDE

        return status

    @staticmethod
    def read_scheme(scheme: dict) -> Tuple:
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

        return obj_scheme


class GameMap(BaseCoordinateSurface):
    __block_width: int = 30
    __block_height: int = 30
    __offset_x: int = 5
    __offset_y: int = 5

    __scheme: Scheme
    __predrawn_surface: BaseCoordinateSurface

    __WIDTH: int = 640
    __HEIGHT: int = 640

    __colors: Dict = {
        "wall" : (46, 82, 152),
        "empty" : (0, 0, 0),
    }

    __SCHEME = {
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

    def __init__(self, x, y):
        super().__init__(x, y, self.__WIDTH, self.__HEIGHT)
        self.__scheme = Scheme(self.__SCHEME)
        self.__predrawn_surface = self.get_predrawn_surface()

    def get_block_width(self) -> int:
        return self.__block_width

    def get_block_height(self) -> int:
        return self.__block_height

    def get_offset_x(self) -> int:
        return self.__offset_x

    def get_offset_y(self) -> int:
        return self.__offset_y

    def get_plan(self) -> tuple:
        return self.__scheme.get_plan()

    def draw(self):
        self.draw_surface(self.__predrawn_surface)

    def get_block(self, map_x: int, map_y: int) -> Block:
        x, y = self.__get_block_coordinates(map_x, map_y)
        status = self.__scheme.get_status(map_x, map_y)
        block = Block(x, y, map_x, map_y, status)
        return block

    def __get_block_coordinates(self, x: int, y: int) -> Tuple[float, float]:
        real_x = self.__offset_x + x * self.__block_width + self.__block_width / 2
        real_y = self.__offset_y + y * self.__block_height + self.__block_height / 2
        return real_x, real_y

    def get_block_by_real_coordinates(self, x: float, y: float) -> Block:
        map_x = int((x - self.__offset_x) // self.__block_width)
        map_y = int((y - self.__offset_y) // self.__block_height)
        block = self.get_block(map_x, map_y)
        return block

    def get_next_block(self, current_block: Block, direction: int) -> Block:
        x_add, y_add = Direction.get_adds(direction)
        block = self.get_block(current_block.get_map_x() + x_add, current_block.get_map_y() + y_add)
        return block

    def get_teleport_block(self, current_block: Block, direction: int) -> Block:
        block = None
        size_x, size_y = self.__scheme.get_size()

        if direction in Direction.X_AXIS:
            if current_block.get_map_x() == -1:
                block = self.get_block(size_x, current_block.get_map_y())
            elif current_block.get_map_x() == size_x:
                block = self.get_block(-1, current_block.get_map_y())
            else:
                raise ObjectMovingException
        elif direction in Direction.Y_AXIS:
            if current_block.get_map_y() == -1:
                block = self.get_block(current_block.get_map_x(), size_y)
            elif current_block.get_map_y() == size_y:
                block = self.get_block(current_block.get_map_x(), -1)
            else:
                raise ObjectMovingException
        else:
            raise NonExistDirectionException

        return block

    def set_object(self, obj: BaseObject, map_x: int, map_y: int):
        block = self.get_block(map_x, map_y)
        obj.set_coordinates(block.get_x(), block.get_y())

    def get_predrawn_surface(self) -> BaseCoordinateSurface:
        predrawn_surface = BaseCoordinateSurface(x=0, y=0, width=self.get_width(), height=self.get_height())
        y = self.__offset_y

        for row in self.__scheme.get_plan():
            x = self.__offset_x

            for block in row:
                color = self.__colors["empty"] if block == BlockStatus.EMPTY else self.__colors["wall"]
                predrawn_surface.draw_rect(
                    color, (x, y, self.__block_width, self.__block_height))
                x += self.__block_width

            y += self.__block_height

        return predrawn_surface