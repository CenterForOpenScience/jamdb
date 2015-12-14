# !/usr/local/bin/python3.5
import iodm

YOUR_USERNAME = 'chris'

nsm = iodm.NamespaceManager()
share_ns = nsm.create_namespace('SHARE', '')

users_col = share_ns.create_collection('users', '')
schema = dict(
        type='jsonschema',
        schema=
        {
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

share_ns.update('users', schema, '', lambda x, y: {**x, **y})

users_col.create('chris', {'username': YOUR_USERNAME, 'password': '$2b$12$iujjM4DtPMWVL1B2roWjBeHzjzxaNEP8HbXxdZwRha/j5Pc8E1n2G'},
                 '')
