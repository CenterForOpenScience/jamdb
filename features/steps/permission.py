from behave import given

from jam import auth


@given('{user} have {permission} permissions to {rtype} {resource}')
def set_permissions(context, user, permission, rtype, resource):
    context.resources[rtype][resource].permissions['user-testing-{}'.format(user)] = auth.Permissions.from_string(permission)


@given('{user} have {permission} permissions')
def set_manager_permissions(context, user, permission):
    context.manager.permissions['user-testing-{}'.format(user)] = getattr(auth.Permissions, permission)


@given('{user} is not logged in')
@given('{user} are not logged in')
def clear_auth(context, user):
    context.ignored_auth.append(user)


@given('{user} is a system user')
@given('{user} are a system user')
def system_auth(context, user):
    context.system_auth.append(user)
