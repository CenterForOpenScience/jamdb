from jam import NamespaceManager
from jam import exceptions
from jam.auth import Permissions


creator = 'tracked-SHARE|users-chris'
# doc_loc = os.path.join(os.path.split(__file__)[0], 'share-docs.json')


def main():
    try:
        ns = NamespaceManager().get_namespace('SHARE')
    except exceptions.NotFound:
        ns = NamespaceManager().create_namespace('SHARE', creator)

    try:
        ns.get_collection('curations')
    except exceptions.NotFound:
        ns.create_collection('curations', creator, permissions={
            '*': Permissions.READ,
            'tracked-SHARE|users-*': Permissions.CREATE
        })

    try:
        ns.get_collection('normalized')
    except exceptions.NotFound:
        ns.create_collection('normalized', creator, permissions={
            '*': Permissions.READ
        })

    try:
        ns.get_collection('authors')
    except exceptions.NotFound:
        ns.create_collection('authors', creator, permissions={
            '*': Permissions.READ
        })

    try:
        collection = ns.get_collection('users')
    except exceptions.NotFound:
        collection = ns.create_collection('users', creator, permissions={
            'tracked-SHARE|users-chris': Permissions.ADMIN
        }, schema={'type': 'jsonschema', 'schema': {
            'id': '/',
            'type': 'object',
            'properties': {
                'username': {
                    'id': 'username',
                    'type': 'string',
                    'pattern': '^\w{1,64}$'
                },
                'password': {
                    'id': 'password',
                    'type': 'string',
                    'pattern': '^\$2b\$1[0-3]\$\S{53}$'
                }
            },
            'required': ['username', 'password']
        }})

    try:
        collection.create('chris', {
            'username': 'chris',
            'password': '$2b$12$iujjM4DtPMWVL1B2roWjBeHzjzxaNEP8HbXxdZwRha/j5Pc8E1n2G'
        }, 'tracked-SHARE|users-chris')
    except exceptions.KeyExists:
        pass

    # with open(doc_loc) as docs:
    #     for card in json.load(docs):
    #         try:
    #             collection.create(card['shareProperties']['docID'], card, '')
    #         except exceptions.KeyExists:
    #             pass


if __name__ == '__main__':
    main()
