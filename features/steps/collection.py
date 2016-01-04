import json

from behave import then
from behave import when
from behave import given

import requests

from jam import auth


@given('collection {collection} exists in namespace {namespace}')
def ensure_collection(context, collection, namespace):
    context.resources['collection'][collection] = context.resources['namespace'][namespace].create_collection(collection, 'user-testing-system')


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
