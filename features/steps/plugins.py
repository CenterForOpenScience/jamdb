import json
from unittest import mock

from sendgrid import SendGridError  # noqa

from behave import then
from behave import given


@then('sendgrid will be called with')
def assert_called(context):
    actual = json.loads(context.text or '{}')
    # Kinda hacky but tokens are time based
    mail = context.mocks['jam.plugins.user.sendgrid'].SendGridClient().send.call_args[0][0]

    mock = context.mocks['jam.plugins.user.sendgrid'].Mail
    mock.assert_called_with(to=actual['to'])

    if actual.get('from'):
        mail.set_from(actual.get('from'))

    token = mail.add_substitution.call_args_list[0][0][1]
    mail.add_substitution.assert_any_call(':token', token)

    user = mail.add_substitution.call_args_list[1][0][1]
    mail.add_substitution.assert_any_call(':user', user)

    mail.add_filter.assert_any_call('templates', 'enable', 1)
    mail.add_filter.assert_any_call('templates', 'template_id', actual['template'])


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
