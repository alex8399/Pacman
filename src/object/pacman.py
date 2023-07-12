from object.base import ManagingObject
from surface.base import BaseSurface

class Pacman(ManagingObject):
    __color : tuple = (238, 210, 75)
    
    def __init__(self, x : float, y : float):
        super().__init__(x, y, 30, 30)
    
    def draw(self, surface : BaseSurface):
        x = int(self.x) - self.height // 2
        y = int(self.y) - self.height // 2
        radious = self.height // 2
        surface.draw_circle(self.__color, (x, y), radious)