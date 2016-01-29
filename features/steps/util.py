import json
import time

from behave import then
from behave import when
from behave import given

import requests

from freezegun import freeze_time

from jam import auth


@when('the content type is {content_type}')
def set_content_type(context, content_type):
    context.content_type = content_type


@when('{user} {method} "{url}"')
def make_request(context, user, method, url):
    headers = {}
    if user not in context.ignored_auth:
        headers['Authorization'] = auth.User.create('user', 'testing', user).token
    headers['Content-Type'] = getattr(context, 'content_type', 'application/vnd.api+json')
    context.response = getattr(requests, method.lower())(context.base_url + url, headers=headers, data=context.text)


@then('the response code will be {:d}')
def response_code(context, code):
    assert context.response.status_code == code, '{} != {}\n{}\n{}'.format(context.response.status_code, code, context.response, context.response.json())


@then('the content type will be "{content_type}"')
def content_type_check(context, content_type):
    expected, actual = context.response.headers['Content-Type'], content_type
    assert expected == actual, '{} != {}'.format(expected, actual)


@given('the time is {ftime}')
def freeze(context, ftime):
    offset = (-time.timezone // 3600)
    context.time = freeze_time(ftime, tz_offset=offset)
    context.time.start()
    time.time.__class__.__call__ = lambda self: self.time_to_freeze().timestamp()


@then('the response will contain')
def response_contains(context):
    expected = json.loads(context.text)

    def dict_compare(src, target):
        for key, value in src.items():
            if isinstance(value, dict):
                dict_compare(value, target[key])
            elif isinstance(value, list):
                for i, subvalue in enumerate(value):
                    if isinstance(subvalue, dict):
                        dict_compare(subvalue, target[key][i])
                    else:
                        assert subvalue == target[key][i], 'Expected "{}", got "{}"'.format(subvalue, target[key][i])
            else:
                assert value == target[key], 'Expected "{}", got "{}"'.format(value, target[key])

    dict_compare(expected, context.response.json())


@then('the headers will contain')
def headers_contains(context):
    for key, value in json.loads(context.text).items():
        assert context.response.headers[key] == value, 'Header {} does not match\n{} != {}'.format(key, value, context.response.headers[key])
