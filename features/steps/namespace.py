from behave import *  # noqa
from iodm import exceptions


@given('namespace {namespace} does not exist')
def remove_namespace(context, namespace):
    try:
        context.manager.delete(namespace, 'user-testing-system')
        del context.resources['namespace'][namespace]
    except exceptions.NotFound:
        pass


@given('namespace {namespace} exists')
@given('namespace {namespace} does exist')
def create_namespace(context, namespace):
    context.resources['namespace'][namespace] = context.manager.create_namespace(namespace, 'user-testing-system')
