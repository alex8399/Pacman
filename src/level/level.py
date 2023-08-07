from level.base import BaseLevel
from level.config import LevelConfig
from utils.window import Window
from utils.clock import Clock

from object.pacman import Pacman
from surface.map import Map


class Level(BaseLevel):
    
    def __init__(self, window: Window, clock: Clock):
        super().__init__(window, clock, LevelConfig())

    def exec(self):
        run = True

        map = Map(x=0, y=0)
        pacman = Pacman(user_device=self.keyboard)
        map.set_object(pacman, 4, 9)
        

        while run:
            self.update_environment()

            for event in self.event_handler.get_events():
                if event.is_exit():
                    self.exit()
            
            pacman.init_user_direction()
            pacman.move(map)
            
            map.draw(map)
            pacman.draw(map)
            map.blit_all(self.window)
            
            self.window.update()
