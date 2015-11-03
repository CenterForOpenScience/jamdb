class IodmException(Exception):
    pass


class BackendException(IodmException):
    pass


class NotFound(BackendException):
    pass
