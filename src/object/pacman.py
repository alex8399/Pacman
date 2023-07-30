from object.moving import ManagingObject
from surface.base import BaseSurface

class Pacman(ManagingObject):
    __color : tuple = (238, 210, 75)
    
    def __init__(self):
        super().__init__(x = 0, y = 0, height = 28, width = 28, speed = 3)
    
    def draw(self, surface : BaseSurface):
        x = int(self.x)
        y = int(self.y)
        radious = self.height // 2
        surface.draw_circle(self.__color, (x, y), radious)