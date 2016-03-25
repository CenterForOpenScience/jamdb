import json

from behave import then
from behave import when
from behave import given

import requests

from jam import auth


@given('collection {collection} exists in namespace {namespace}')
def ensure_collection(context, collection, namespace):
    context.resources['collection'][collection] = context.resources['namespace'][namespace].create_collection(collection, 'user-testing-system')

    if context.text:
        context.resources['namespace'][namespace].update(collection, [
            {'op': 'add', 'path': '/{}'.format(key), 'value': value}
            for key, value in json.loads(context.text).items()
        ], 'user-testing-system')


@when('{user} create collection {collection} in namespace {namespace}')
def create_collection(context, user, collection, namespace):
    headers = {}
    if user not in context.ignored_auth:
        headers['Authorization'] = auth.User.create('user', 'testing', user).token

    context.response = requests.post(
        context.base_url + '/v1/namespaces/{}/collections'.format(namespace),
        headers=headers,
        data=json.dumps({'data': {
            'id': collection,
            'type': 'collections',
            'attributes': {
            }
        }})
    )


@given('the {plugin} plugin is enabled for collection {collection_id}')
def enable_plugin(context, plugin, collection_id):
    namespace, collection = collection_id.split('.')

    context.resources['namespace'][namespace].update(collection, [{
        'op': 'add',
        'value': json.loads(context.text or '{}'),
        'path': '/plugins/{}'.format(plugin),
    }], 'user-testing-system')
