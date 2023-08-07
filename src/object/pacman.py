from object.moving import ManagingKeyboardObject
from surface.base import BaseSurface

class Pacman(ManagingKeyboardObject):
    __color : tuple = (238, 210, 75)
    
    def __init__(self, *args, **kwargs):
        keyboard = kwargs.get("user_device")
        super().__init__(x = 0, y = 0, height = 24, width = 24, speed = 1, user_device = keyboard)
    
    def draw(self, surface : BaseSurface):
        x = int(self.x)
        y = int(self.y)
        radious = self.height // 2
        surface.draw_circle(self.__color, (x, y), radious)