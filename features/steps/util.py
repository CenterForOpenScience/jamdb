import json
import time

from behave import then
from behave import when
from behave import given

import nose

import requests

from freezegun import freeze_time

from jam import auth


# Hack to print full diffs
nose.tools.assert_equal.__self__.maxDiff = None


@when('the content type is {content_type}')
def set_content_type(context, content_type):
    context.content_type = content_type


@when('{user} {method} "{url}"')
@when('{user} {method} to "{url}"')
def make_request(context, user, method, url):
    headers = {}
    if user in context.system_auth:
        headers['Authorization'] = auth.User.create('system', 'system', user).token
    elif user not in context.ignored_auth:
        headers['Authorization'] = auth.User.create('user', 'testing', user).token
    headers['Content-Type'] = getattr(context, 'content_type', 'application/vnd.api+json')
    context.response = getattr(requests, method.lower())(context.base_url + url, headers=headers, data=(context.text and context.text.encode('utf-8')) or context.text)


@then('the response code will be {:d}')
def response_code(context, code):
    nose.tools.assert_equal(context.response.status_code, code)


@then('the content type will be "{content_type}"')
def content_type_check(context, content_type):
    expected, actual = context.response.headers['Content-Type'], content_type
    nose.tools.assert_equal(expected, actual)


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
                        nose.tools.assert_equal(subvalue, target[key][i])
            else:
                nose.tools.assert_equal(value, target[key])

    dict_compare(expected, context.response.json())


@then('the response will be')
def response_exact(context):
    expected = json.loads(context.text)
    nose.tools.assert_equal(expected, context.response.json())


@then('the headers will contain')
def headers_contains(context):
    for key, value in json.loads(context.text).items():
        nose.tools.assert_equal(context.response.headers[key], value)


@given('the URL "{uri}" responds {status:d}')
def patch_url(context, uri, status):
    aiohttpretty.register_json_uri('GET', uri, status=status, body=json.loads(context.text or '{}'))


@given('the URL "{uri}" responds {status:d} to {method}s')
def patch_url_method(context, uri, status, method):
    aiohttpretty.register_json_uri(method.upper(), uri, status=status, body=json.loads(context.text or '{}'))


@then('the URL "{uri}" will have been {method}ed')
def assert_url_hit(context, uri, method):
    args = {
        'uri': uri,
        'method': method
    }
    if context.text:
        args['data'] = json.dumps(json.loads(context.text))  # For formatting
    assert aiohttpretty.has_call(**args)


@then('my JWT will contain')
def jwt_equals(context):
    expected = json.loads(context.text or '{}')
    user = auth.User(context.response.json()['data']['attributes']['token'])

    nose.tools.assert_equal(expected, {
        key: value
        for key, value in user.jwt.items()
        if key in expected
    })
