# !/usr/local/bin/python3.5
import jam
import jam.auth

nsm = jam.NamespaceManager()

try:
    share_ns = nsm.create_namespace('OPENTRIALS', 'tracked-OPENTRIALS|users-scrapi')
except jam.exceptions.KeyExists:
    share_ns = nsm.get_namespace('OPENTRIALS')

try:
    users_col = share_ns.create_collection('share-contributor', 'tracked-OPENTRIALS|users-scrapi', permissions={
        '*': jam.auth.Permissions.READ
    })
except jam.exceptions.KeyExists:
    pass

try:
    share_ns.create_collection('share-data', 'tracked-OPENTRIALS|users-scrapi', permissions={
        '*': jam.auth.Permissions.READ
    })
except jam.exceptions.KeyExists:
    pass

try:
    share_ns.create_collection('opentrials-data', 'tracked-OPENTRIALS|users-scrapi', permissions={
        'tracked-OPENTRIALS|users-scrapi': jam.auth.Permissions.ADMIN
    })
except jam.exceptions.KeyExists:
    pass


try:
    share_ns.create_collection('contributor-curation', 'tracked-OPENTRIALS|users-scrapi', permissions={
        'user-osf-*': jam.auth.Permissions.CREATE
    })
except jam.exceptions.KeyExists:
    share_ns.update('contributor-curation', [{
        'op': 'add', 'path': '/permissions/user-osf-*', 'value': jam.auth.Permissions.CREATE
    }], 'tracked-OPENTRIALS|users-scrapi')

try:
    users_col = share_ns.create_collection('users', 'tracked-OPENTRIALS|users-scrapi')
except jam.exceptions.KeyExists:
    users_col = share_ns.get_collection('users')

schema = dict(
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
