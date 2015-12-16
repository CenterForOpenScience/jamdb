# !/usr/local/bin/python3.5
import iodm

USERNAME = 'chris'

nsm = iodm.NamespaceManager()

try:
    share_ns = nsm.create_namespace('SHARE', '')
except iodm.exceptions.KeyExists:
    share_ns = nsm.get_namespace('SHARE')

try:
    users_col = share_ns.create_collection('users', '')
except iodm.exceptions.KeyExists:
    users_col = share_ns.get_collection('users')

schema = dict(
    schema=dict(
        type='jsonschema',
        schema={
            "id": "/",
            "type": "object",
            "properties": {
                "username": {
                    "id": "username",
                    "type": "string",
                    "pattern": "^\w{1,64}$"
                },
                "password": {
                    "id": "password",
                    "type": "string",
                    "pattern": "^\$2b\$1[0-3]\$\S{53}$"
                }
            },
            "required": [
                "username",
                "password"
            ]
        }
    )
)

share_ns.update('users', schema, '', lambda x, y: {**x, **y})

users_col.create(
    USERNAME, {
        'username': USERNAME,
        'password': '$2b$12$iujjM4DtPMWVL1B2roWjBeHzjzxaNEP8HbXxdZwRha/j5Pc8E1n2G'
    }, ''
)
