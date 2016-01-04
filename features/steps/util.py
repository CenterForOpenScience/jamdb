import json
import time

from behave import then
from behave import when
from behave import given

import requests

from freezegun import freeze_time

from iodm import auth


@when('{user} {method} "{url}"')
def make_request(context, user, method, url):
    headers = {}
    if user not in context.ignored_auth:
        headers['Authorization'] = auth.User.create('user', 'testing', user).token
    context.response = getattr(requests, method.lower())(context.base_url + url, headers=headers, data=context.text)


@then('the response code will be {:d}')
def response_code(context, code):
    assert context.response.status_code == code, '{} != {}\n{}\n{}'.format(context.response.status_code, code, context.response, context.response.json())


@given('the time is {ftime}')
def freeze(context, ftime):
    offset = (-time.timezone//3600)
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
