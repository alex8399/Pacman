class BaseException(Exception):
    pass


class ExitException(BaseException):
    '''Raise when user clicks exit button'''
    pass


class NonExistDirectionException(BaseException):
    '''Raise when non-exist number of direction is indicated'''
    pass


class NegativeSpeedException(BaseException):
    '''Raise when negative speed is indicated'''
    pass
