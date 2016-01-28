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


class BadRequest(JamException):
    should_log = False
    status = http.client.BAD_REQUEST
    title = 'Bad request'


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
    title = 'Invalid type'
    status = http.client.BAD_REQUEST

    def __init__(self, field, expected, value):
        super().__init__(detail='Expected field {} to be of type {}. Got {}'.format(field, expected, value))


class IncorrectParameter(JamException):
    should_log = False
    title = 'Incorrect Paramter'
    status = http.client.BAD_REQUEST

    def __init__(self, field, expected, value):
        super().__init__(detail='Expected field {} to be {}. Got {}'.format(field, expected, value))


class MissingExtension(JamException):
    should_log = False
    title = 'Missing extension'
    status = http.client.UNSUPPORTED_MEDIA_TYPE

    def __init__(self, extension):
        super().__init__(
            detail='Expected Content-Type to contain ext="{}";'.format(extension)
        )


class JsonPatchTestFailed(JamException):
    should_log = False
    title = 'Json patch test failed'
    status = http.client.PRECONDITION_FAILED

    def __init__(self, exception):
        super().__init__(detail=str(exception))


class NoSuchSchema(JamException):
    should_log = False
    code = 'C400'
    title = 'Invalid schema type'
    status = http.client.BAD_REQUEST

    def __init__(self, name):
        super().__init__(detail='"{}" is not a valid schema type'.format(name))


class InvalidSchema(JamException):
    should_log = False
    code = 'C400'
    title = 'Invalid schema'
    status = http.client.BAD_REQUEST

    def __init__(self, type_):
        super().__init__(detail='The supplied data was an invalid {} schema '.format(type_))


class InvalidPermission(JamException):
    should_log = False
    code = 'P400'
    title = 'Invalid permission'
    status = http.client.BAD_REQUEST

    def __init__(self, permission):
        super().__init__(detail='"{}" is not a valid permission level'.format(permission))


class InvalidField(JamException):
    should_log = False
    title = 'Invalid field'
    status = http.client.BAD_REQUEST

    def __init__(self, field):
        super().__init__(detail='Values at "{}" may not be altered'.format(field))


class SchemaValidationFailed(JamException):
    should_log = False
    title = 'Schema validation failed'
    code = 'S400'
    status = http.client.BAD_REQUEST

    def __init__(self, detail):
        super().__init__(detail=detail)
