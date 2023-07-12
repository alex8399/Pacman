from surface.base import BaseSurface, MixinDrawingSurace

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

EMPTY_BLOCK_COLOR = (0, 0, 0)
WALL_BLOCK_COLOR = (65, 99, 149)


class BaseMap(BaseSurface):
    __block_width: int
    __block_height: int
    __map: list
    __predrawn_surface: BaseSurface

    def __init__(self, x: int, y: int, width: int, height: int, block_width: int, block_height: int, map_plan: list):
        super().__init__(x, y, width, height)
        self.__block_width = block_width
        self.__block_height = block_height
        self.__map = map_plan

        self.__predraw()

    def __predraw(self):
        self.__predrawn_surface = BaseSurface(
            self.x, self.y, self.width, self.height)

        x = 0
        y = 0

        for row in self.__map:
            x = 0

            for block in row:
                color = EMPTY_BLOCK_COLOR if block == EMPTY_BLOCK else WALL_BLOCK_COLOR
                self.__predrawn_surface.draw_rect(color, (x, y, self.__block_width, self.__block_height))
                x += self.__block_width

            y += self.__block_height

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


class Map(BaseMap):

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 608, 608, 32, 32, MAP_PLAN)
