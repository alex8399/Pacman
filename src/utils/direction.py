from exception import NonExistDirectionException


class Direction:
    LEFT: int = 0
    UP: int = 1
    RIGHT: int = 2
    DOWN: int = 3

    X_AXIS: tuple = (LEFT, RIGHT)
    Y_AXIS: tuple = (UP, DOWN)

    @staticmethod
    def get_adds(direction: int) -> (int, int):
        x_add = y_add = 0

        if direction == Direction.RIGHT:
            x_add = 1
        elif direction == Direction.LEFT:
            x_add = -1
        elif direction == Direction.DOWN:
            y_add = 1
        elif direction == Direction.UP:
            y_add = -1
        else:
            raise NonExistDirectionException

        return x_add, y_add
