import json

from behave import when
from behave import given

import requests

from jam import auth


@given('document {document} exists in {namespace}/{collection}')
def ensure_document(context, document, namespace, collection):
    data = json.loads(context.text or "{}")
    doc = context.resources['collection'][collection].create(document, data, 'user-testing-system')
    context.resources['document'][document] = doc


@when('{user} create document {document} in {namespace}/{collection}')
def create_collection(context, user, document, namespace, collection):
    headers = {}
    if user not in context.ignored_auth:
        headers['Authorization'] = auth.User.create('user', 'testing', user).token

    context.response = requests.post(
        context.base_url + '/v1/namespaces/{}/collections/{}/documents'.format(namespace, collection),
        headers=headers,
        data=json.dumps({'data': {
            'id': document,
            'type': 'documents',
            'attributes': json.loads(context.text or "{}")
        }})
    )
