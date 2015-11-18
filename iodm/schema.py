import abc

import jsonschema


def get_schema(name):
    try:
        return next(x for x in Schema.__subclasses__() if x.name == name)
    except StopIteration:
        raise Exception('No such schema')


class Schema(abc.ABC):

    def __init__(self, schema):
        self._schema = schema

    def validate(self, data):
        raise NotImplemented


class JSONSchema(Schema):

    name = 'jsonschema'

    def __init__(self, schema):
        jsonschema.Draft4Validator.check_schema(schema)
        super().__init__(schema)

    def validate(self, data):
        # TODO Translate to custom exceptions
        jsonschema.validate(data, self._schema)
