from src.pacman.objects.moving_object import KeyboardObject
from src.engine.surface import BaseSurface
from src.engine.utils.IOdevices import KeyBoard

from src.pacman.surfaces.map import GameMap

class Pacman(KeyboardObject):
    __color : tuple = (238, 210, 75)
    
    def __init__(self, keyboard: KeyBoard, game_map: GameMap):
        super().__init__(x = 0, y = 0, height = 24, width = 24, speed = 1, game_map=game_map, keyboard=keyboard)
    
    def draw(self, surface : BaseSurface):
        x = int(self.get_x())
        y = int(self.get_y())
        radious = self.get_height() // 2
        surface.draw_circle(self.__color, (x, y), radious)