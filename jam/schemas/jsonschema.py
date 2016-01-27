import jsonschema

from jam import exceptions
from jam.schemas.base import BaseSchema


class JSONSchema(BaseSchema):

    @classmethod
    def validate_schema(self, schema):
        try:
            jsonschema.Draft4Validator.check_schema(schema)
        except jsonschema.SchemaError:
            raise exceptions.InvalidSchema('jsonschema')

    def validate(self, data):
        # TODO Translate to custom exceptions
        jsonschema.validate(data, self._schema)
