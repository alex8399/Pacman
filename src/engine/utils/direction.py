from src.engine.exceptions import NonExistDirectionException


class Direction:
    """
    Class represents direction, contains methods to work with directions.
    Directions are represented as integer constants.
    """

    LEFT: int = 0
    UP: int = 1
    RIGHT: int = 2
    DOWN: int = 3

    X_AXIS: tuple = (LEFT, RIGHT)
    Y_AXIS: tuple = (UP, DOWN)

    __MIN_VALUE: int = LEFT
    __MAX_VALUE: int = DOWN

    @staticmethod
    def is_valid_direction(direction: int) -> bool:
        """Define if direction is valid."""
        return __class__.__MIN_VALUE <= direction <= __class__.__MAX_VALUE

    @staticmethod
    def get_adds(direction: int) -> (int, int):
        """Get addition to x, y-coordinates based on direction."""
        x_add = y_add = 0

        if direction == __class__.RIGHT:
            x_add = 1
        elif direction == __class__.LEFT:
            x_add = -1
        elif direction == __class__.DOWN:
            y_add = 1
        elif direction == __class__.UP:
            y_add = -1
        else:
            raise NonExistDirectionException

        return x_add, y_add
