# !/usr/local/bin/python3.5
import jam
import jam.auth

nsm = jam.NamespaceManager()

try:
    share_ns = nsm.create_namespace('SHARE', 'tracked-SHARE|users-scrapi')
except jam.exceptions.KeyExists:
    share_ns = nsm.get_namespace('SHARE')

try:
    users_col = share_ns.create_collection('share-contributor', 'tracked-SHARE|users-scrapi', permissions={
        '*': jam.auth.Permissions.READ
    })
except jam.exceptions.KeyExists:
    pass

try:
    share_ns.create_collection('share-data', 'tracked-SHARE|users-scrapi', permissions={
        '*': jam.auth.Permissions.READ
    })
except jam.exceptions.KeyExists:
    pass

try:
    share_ns.create_collection('contributor-curation', 'tracked-SHARE|users-scrapi', permissions={
        'user-osf-*': jam.auth.Permissions.CREATE
    })
except jam.exceptions.KeyExists:
    share_ns.update('contributor-curation', [{
        'op': 'add', 'path': '/permissions/user-osf-*', 'value': jam.auth.Permissions.CREATE
    }], 'tracked-SHARE|users-scrapi')

try:
    users_col = share_ns.create_collection('users', 'tracked-SHARE|users-scrapi')
except jam.exceptions.KeyExists:
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

share_ns.update('users', [{'op': 'add', 'path': '/schema', 'value': schema}], 'system')

for username in ('chris', 'scrapi'):
    try:
        users_col.create(
            username, {
                'username': username,
                'password': '$2b$12$iujjM4DtPMWVL1B2roWjBeHzjzxaNEP8HbXxdZwRha/j5Pc8E1n2G'
            }, ''
        )
    except jam.exceptions.KeyExists:
        print('\nUser {user} already exists in the users collection'.format(user=username))
