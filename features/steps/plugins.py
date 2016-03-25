import json
import nose
from unittest import mock

from mandrill import Error as MandrillError  # noqa

from behave import then
from behave import given


@then('mandrill will be called with')
def assert_called(context):
    actual = json.loads(context.text or '{}')
    # Kinda hacky but tokens are time based
    mock = context.mocks['jam.plugins.user.mandrill'].Mandrill().messages.send_template
    actual['template_content'][0]['token'] = mock.call_args[1]['template_content'][0]['token']

    nose.tools.assert_equals(mock.call_args[1], actual)


@given('we mock {module}')
def mock_it(context, module):
    patcher = mock.patch(module)
    context.patches[module] = patcher
    context.mocks[module] = patcher.start()


@given('{module} will throw {error}')
def side_effects(context, module, error):
    patcher = mock.patch(module)
    context.patches[module] = patcher

    context.mocks[module] = patcher.start()
    context.mocks[module].side_effect = globals()[error]
