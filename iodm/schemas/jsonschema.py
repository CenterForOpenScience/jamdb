import jsonschema

from iodm.schemas.base import BaseSchema


class JSONSchema(BaseSchema):

    @classmethod
    def validate_schema(self, schema):
        jsonschema.Draft4Validator.check_schema(schema)

    def validate(self, data):
        # TODO Translate to custom exceptions
        jsonschema.validate(data, self._schema)
