import jsonschema
from jam import exceptions
from jam.server.api.jsonapi import schemas


def parse(method, payload, extensions=()):
    return {
        'PUT': _parse_put,
        'POST': _parse_post,
        'PATCH': _parse_patch,
    }[method](payload, extensions)


def _parse_patch(payload, extensions):
    # I'm so sorry. Minimizes the amount of code needed for this check.
    # JsonPatch must have a list anything else must have a dict
    if ('jsonpatch' in extensions) ^ isinstance(payload, list):
        if isinstance(payload, list):
            raise exceptions.MissingExtension('jsonpatch')  # Got a list with incorrect Content-Type
        else:
            raise exceptions.InvalidParameterType('', 'list', dict)  # Got a dict with jsonpatch

    if isinstance(payload, list):
        return JsonPatchPayload.parse(payload)
    return JsonAPIPayload.parse(payload)


def _parse_put(payload, extensions):
    return JsonAPIPayload.parse(payload)


def _parse_post(payload, extensions):
    if not isinstance(payload, dict):
        raise exceptions.InvalidParameterType('', 'object', type(payload))

    if not isinstance(payload.get('data'), (list, dict)):
            raise exceptions.InvalidParameterType('data', 'list or object', type(payload.get('data')))

    # I'm so sorry. Minimizes the amount of code needed for this check.
    # Bulk must have a list anything else must have a dict
    if ('bulk' in extensions) ^ isinstance(payload['data'], list):
        if isinstance(payload['data'], list):
            raise exceptions.MissingExtension('bulk')  # Got a list with incorrect Content-Type
        else:
            raise exceptions.InvalidParameterType('data', 'list', type(payload['data']))  # Got a dict with bulk

    if isinstance(payload['data'], list):
        return BulkPayload.parse(payload)
    return JsonAPIPayload.parse(payload)


class BaseJsonAPIPayload:
    SCHEMA = None

    @classmethod
    def parse(cls, payload):
        try:
            jsonschema.validate(payload, cls.SCHEMA)
        except jsonschema.ValidationError as e:
            raise exceptions.BadRequestBody(e)
        return cls(payload)

    def __init__(self, raw):
        self._raw = raw


class JsonAPIPayload(BaseJsonAPIPayload):
    SCHEMA = schemas.JSONAPI_SCHEMA

    def __init__(self, payload):
        super().__init__(payload)
        data = payload['data']
        data['id'] = data.get('id')
        self.__dict__.update(data)


class JsonPatchPayload(BaseJsonAPIPayload):
    SCHEMA = schemas.JSONPATCH_SCHEMA

    def __init__(self, payload):
        super().__init__(payload)
        self.patches = payload


class BulkPayload(BaseJsonAPIPayload):
    SCHEMA = schemas.BULK_SCHEMA

    def __init__(self, payload):
        super().__init__(payload)
        self.payloads = [
            JsonAPIPayload({'data': pay})
            for pay in payload['data']
        ]
