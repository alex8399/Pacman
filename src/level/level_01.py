from level.base import BaseLevel
from level.config import LevelConfig
from utils.window import Window
from utils.clock import Clock

from object.pacman import Pacman
from surface.map import Map


class Level01(BaseLevel):
    
    def __init__(self, window: Window, clock: Clock):
        super().__init__(window, clock, LevelConfig())

    def exec(self):
        run = True

        map = Map(x=0, y=32)
        pacman = Pacman()
        map.set_object(pacman, 1, 1)
        

        while run:
            self.update_environment()

            for event in self.event_handler.get_events():
                if event.is_exit():
                    self.exit()
            
            
            pacman.init_user_direction(self.keyboard)
            pacman.move(map)

            map.draw(map)
            pacman.draw(map)

            map.build(self.window)
            self.window.update()
