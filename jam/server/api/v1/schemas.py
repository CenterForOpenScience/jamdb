JSONPATCH_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'object',
        'required': ['op', 'path'],
        'path': {'type': 'string'},
        'oneOf': [{
            'required': ['value'],
            'properties': {
                'op': {
                    'description': 'The operation to perform.',
                    'type': 'string',
                    'enum': ['add', 'replace', 'test']
                },
                'value': {
                    'description': 'The value to add, replace or test.'
                }
            }
        }, {
            'properties': {
                'op': {
                    'description': 'The operation to perform.',
                    'type': 'string',
                    'enum': ['remove']
                }
            }
        }, {
            'required': ['from'],
            'properties': {
                'op': {
                    'description': 'The operation to perform.',
                    'type': 'string',
                    'enum': ['move', 'copy']
                },
                'from': {
                    'description': 'A JSON Pointer path pointing to the locatoin to move/copy from.',
                    'type': 'string'
                }
            }
        }]
    }
}


JSONAPI_INNER_SCHEMA = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'type': {'type': 'string'},
        'attributes': {'type': 'object'},
        'meta': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'created-by': {'type': 'string'}
            }
        },
    },
    'additionalProperties': False,
    'required': ['attributes', 'type'],
}


BULK_SCHEMA = {
    'type': 'array',
    'items': JSONAPI_INNER_SCHEMA
}


BODY_SCHEMAS = {
    ('POST', list): BULK_SCHEMA,
    ('POST', dict): JSONAPI_INNER_SCHEMA,
    ('PUT', dict): {
        'type': 'object',
        'properties': {
            'data': JSONAPI_INNER_SCHEMA
        },
        'required': ['data'],
        'additionalProperties': False
    },
    ('PATCH', dict): {
        'type': 'object',
        'properties': {
            'data': JSONAPI_INNER_SCHEMA
        },
        'required': ['data'],
        'additionalProperties': False
    },
    ('PATCH', list): JSONPATCH_SCHEMA
}
