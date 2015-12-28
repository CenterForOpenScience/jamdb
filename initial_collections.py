# !/usr/local/bin/python3.5
import iodm
import iodm.auth

nsm = iodm.NamespaceManager()

try:
    share_ns = nsm.create_namespace('SHARE', 'tracked-SHARE|users-scrapi')
except iodm.exceptions.KeyExists:
    share_ns = nsm.get_namespace('SHARE')

try:
    users_col = share_ns.create_collection('share-contributor', 'tracked-SHARE|users-scrapi', permissions={
        '*': iodm.auth.Permissions.READ
    })
except iodm.exceptions.KeyExists:
    pass

try:
    share_ns.create_collection('share-data', 'tracked-SHARE|users-scrapi', permissions={
        '*': iodm.auth.Permissions.READ
    })
except iodm.exceptions.KeyExists:
    pass

try:
    users_col = share_ns.create_collection('users', 'tracked-SHARE|users-scrapi')
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

for username in ('chris', 'scrapi'):
    try:
        users_col.create(
            username, {
                'username': username,
                'password': '$2b$12$iujjM4DtPMWVL1B2roWjBeHzjzxaNEP8HbXxdZwRha/j5Pc8E1n2G'
            }, ''
        )
    except iodm.exceptions.KeyExists:
        print('\nUser {user} already exists in the users collection'.format(user=username))
