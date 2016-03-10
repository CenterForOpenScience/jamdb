import json

import jsonschema

from jam import exceptions
from jam.util import order_dictionary
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
        try:
            jsonschema.validate(data, self._schema)
        except jsonschema.ValidationError as e:
            raise exceptions.SchemaValidationFailed(
                'Validation error "{}" at "{}" against schema "{}"'.format(
                    e.message,
                    '/'.join(e.absolute_path),
                    json.dumps(order_dictionary(e.schema))
                )
            )
