# python scripts/gen_schemas.py && raml2html api.raml > ...
import os
import json
import yaml

HERE = os.path.dirname(__file__)

META = {
    'meta': {
        'modified-by': {
            'type': 'string',
            'pattern': r'^.+\-.*\-.+$'
        },
        'created-by': {
            'type': 'string',
            'pattern': r'^.+\-.*\-.+$'
        },
        'modified-on': {
            'type': 'string',
            'format': 'date-time',
        },
        'create-on': {
            'type': 'string',
            'format': 'date-time',
        },
    }
}


ID = {
    'type': 'string',
    'pattern': r'[\d\w\.\-]{3,64}'
}

SINGLE = {
    'data': {
        'attributes': None,
        'required': ['attributes'],
        'additionalProperties': False,
    },
    # 'meta': META,
    'required': ['data'],
    'additionalProperties': False,
}

MULTIPLE = {
    'data': {
        'type': 'array',
        'items': None
    },
    'links': {
        'type': 'object'
    },
    'meta': {
        'type': 'object',
        'properties': {
            'total': {
                'id': 'total',
                'type': 'integer'
            },
            'perPage': {
                'id': 'total',
                'type': 'integer'
            }
        }
    }
}


for resource in ('Namespace', 'Collection', 'Document', 'History'):
    with open(os.path.join(HERE, '../schemas/{}.yml'.format(resource)), 'r') as fobj:
        schema = yaml.load(fobj.read())

    SINGLE['data'].pop('id', None)
    SINGLE['data']['attributes'] = {'type': 'object', 'properties': schema}
    with open(os.path.join(HERE, '../schemas/{}-update.json'.format(resource)), 'w') as fobj:
        json.dump(SINGLE, fobj, indent=4)

    SINGLE['data']['attributes']['required'] = list(SINGLE['data']['attributes'].keys())
    with open(os.path.join(HERE, '../schemas/{}-replace.json'.format(resource)), 'w') as fobj:
        json.dump(SINGLE, fobj, indent=4)

    SINGLE['data']['id'] = ID
    with open(os.path.join(HERE, '../schemas/{}-create.json'.format(resource)), 'w') as fobj:
        json.dump(SINGLE, fobj, indent=4)

    SINGLE['meta'] = META
    with open(os.path.join(HERE, '../schemas/{}-multiple.json'.format(resource)), 'w') as fobj:
        json.dump(SINGLE, fobj, indent=4)

    MULTIPLE['data'] = SINGLE
    with open(os.path.join(HERE, '../schemas/{}-single.json'.format(resource)), 'w') as fobj:
        json.dump(MULTIPLE, fobj, indent=4)
