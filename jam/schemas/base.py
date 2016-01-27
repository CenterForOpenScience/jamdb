import abc


class BaseSchema(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def validate_schema(self, schema):
        raise NotImplemented

    def __init__(self, schema):
        self.__class__.validate_schema(schema)
        self._schema = schema

    @abc.abstractmethod
    def validate(self, data):
        raise NotImplemented
