import abc


class BaseSchema(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def validate_schema(self, schema):
        raise NotImplemented

    def __init__(self, schema):
        self._schema = schema

    @abc.abstractmethod
    def validate(self, data):
        raise NotImplemented
