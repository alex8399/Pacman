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

class ObjectMovingException(BaseException):
    '''Raise when error occurs in object moving'''
    pass


class StatusBlockNonExistException(BaseException):
    '''Raise when block status does not exist'''
    pass


class IODeviceException(BaseException):
    '''Raise when Exception is thrown from IO device'''
    pass