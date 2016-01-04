import http.client


class JamException(Exception):
    code = None
    detail = None
    should_log = True
    status = http.client.INTERNAL_SERVER_ERROR
    title = 'An error has occured'

    def __init__(self, code=None, status=None, title=None, detail=None):
        self.title = title or self.__class__.title
        self.status = status or self.__class__.status

        self.code = code or self.__class__.code or str(int(self.status))
        self.detail = detail or self.__class__.detail or self.title

    def serialize(self):
        return {
            'code': self.code,
            'detail': self.detail,
            'status': str(int(self.status)),
            'title': self.title,
        }

    def __repr__(self):
        return '<{}({}, {})>'.format(self.__class__.__name__, self.status, self.title)

    __str__ = __repr__


class BackendException(JamException):
    pass


class NotFound(BackendException):
    should_log = False
    title = 'Resource not found'
    status = http.client.NOT_FOUND


class KeyExists(BackendException):
    should_log = False
    status = http.client.CONFLICT
    title = 'Resource already exists'


class Forbidden(JamException):
    should_log = False
    status = http.client.FORBIDDEN
    title = 'Forbidden'

    def __init__(self, required, **kwargs):
        super().__init__(
            detail='{} permission or higher is required to perform this action'.format(
                str(required).split('.')[1]
            ),
            **kwargs
        )


class Unauthorized(JamException):
    should_log = False

    def __init__(self, message=None):
        super().__init__(message or 'Unauthorized', http.client.UNAUTHORIZED)


class MalformedData(JamException):
    should_log = False
    title = 'Malformed data'
    status = http.client.BAD_REQUEST


class InvalidParameterType(JamException):
    should_log = False

    def __init__(self, field, expected, value):
        super().__init__('Expected field {} to be of type {}. Got {}'.format(field, expected, type(value)), http.client.BAD_REQUEST)


class IncorrectParameter(JamException):
    should_log = False

    def __init__(self, field, expected, value):
        super().__init__('Expected field {} to be {}. Got {}'.format(field, expected, value), http.client.BAD_REQUEST)
