from behave import given

from jam import auth


@given('{user} have {permission} permissions to {rtype} {resource}')
def set_permissions(context, user, permission, rtype, resource):
    context.resources[rtype][resource].permissions['user-testing-{}'.format(user)] = getattr(auth.Permissions, permission)


@given('{user} is not logged in')
def clear_auth_is(context, user):
    context.ignored_auth.append(user)


@given('{user} are not logged in')
def clear_auth_are(context, user):
    context.ignored_auth.append(user)
