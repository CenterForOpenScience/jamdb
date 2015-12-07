from behave import *  # noqa
from iodm import auth
from iodm import exceptions
import requests


@given('namespace {namespace} does not exist')
def remove_namespace(context, namespace):
    try:
        context.manager.delete(namespace, '---')
        del context['resources'][namespace]
    except exceptions.NotFound:
        pass


@given('namespace {namespace} does exist')
def create_namespace(context, namespace):
    context.resources[namespace] = context.manager.create_namespace(namespace, '---')


@given('{user} have {permission} permissions to {resource}')
def set_permissions(context, user, permission, resource):
    context.resources[resource].permissions['user-testing-{}'.format(user)] = getattr(auth.Permissions, permission)


@given('{user} is not logged in')
def clear_auth_is(context, user):
    context.ignored_auth.append(user)


@given('{user} are not logged in')
def clear_auth_are(context, user):
    context.ignored_auth.append(user)


@when('{user} {method} "{url}"')
def make_request(context, user, method, url):
    headers = {}
    if user not in context.ignored_auth:
        headers['Authorization'] = auth.User.create('user', 'test', user).token
    context.response = getattr(requests, method.lower())(context.base_url + url, headers=headers)


@then('the response code will be {:d}')
def response_code(context, code):
    assert context.response.status_code == code, '{} != {}'.format(context.response.status_code, code)
