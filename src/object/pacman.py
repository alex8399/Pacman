from object.base import ManagingObject
from surface.base import BaseSurface

class Pacman(ManagingObject):
    color : tuple = (255, 0, 0)
    
    def draw(self, surface : BaseSurface):
        self.draw_circle(surface, self.color, self.x, self.y, self.height)