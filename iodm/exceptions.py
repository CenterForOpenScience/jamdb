import json
import http.client


class IodmException(Exception):
    def __init__(self, message, code=http.client.INTERNAL_SERVER_ERROR):
        super().__init__(code)
        self.code = code
        if isinstance(message, dict):
            self.data = message
            self.message = json.dumps(message)
        else:
            self.data = None
            self.message = message

    def __repr__(self):
        return '<{}({}, {})>'.format(self.__class__.__name__, self.code, self.message)

    def __str__(self):
        return '{}, {}'.format(self.code, self.message)


class BackendException(IodmException):
    pass


class NotFound(BackendException):

    def __init__(self, message=None):
        super().__init__(message or 'Resource not found', http.client.NOT_FOUND)


class KeyExists(BackendException):

    def __init__(self, message=None):
        super().__init__(message or 'Resource already exists', http.client.CONFLICT)


class InsufficientPermissions(IodmException):

    def __init__(self, message=None):
        super().__init__(message or 'You do not have sufficient permissions to access this resource', http.client.FORBIDDEN)


class Unauthorized(IodmException):

    def __init__(self, message=None):
        super().__init__(message or 'Unauthorized', http.client.UNAUTHORIZED)
