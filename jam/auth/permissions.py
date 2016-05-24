import sys
import enum
import operator
import functools

from jam import exceptions


class Permissions(enum.IntEnum):
    NONE = 0x0

    CREATE = 0x1
    READ = 0x1 << 1
    UPDATE = 0x1 << 2
    DELETE = 0x1 << 3

    CU = CREATE | UPDATE
    CUD = CU | DELETE
    CR = CREATE | READ
    CRU = CR | UPDATE
    CRUD = CRU | DELETE

    CD = CREATE | DELETE
    RU = READ | UPDATE
    RUD = RU | DELETE
    RD = READ | DELETE

    READ_WRITE = CREATE | READ | UPDATE

    ADMIN = sys.maxsize  # Grants all possible permission

    @classmethod
    def from_method(cls, http_method):
        return {
            'POST': Permissions.CREATE,
            'GET': Permissions.READ,
            'PUT': Permissions.UPDATE,
            'PATCH': Permissions.UPDATE,
            'DELETE': Permissions.DELETE,
            'OPTIONS': Permissions.NONE
        }[http_method.upper()]

    @classmethod
    def from_string(cls, permission):
        try:
            return Permissions(functools.reduce(operator.or_, [
                Permissions[p.strip()]
                for p in permission.split(',')
            ], Permissions.NONE))
        except (AttributeError, KeyError):
            raise exceptions.InvalidPermission(permission)

    @classmethod
    def get_permissions(cls, user, *perm_objs):
        if user and (user.granted or user.limited):
            ref = ''
            for obj in perm_objs:
                ref += obj.ref
                if user.limited:
                    obj.permissions = {user.uid: user.granted.get(ref, Permissions.NONE)}
                else:
                    obj.permissions[user.uid] = obj.permissions.get(user.uid, Permissions.NONE) | user.granted.get(ref, Permissions.NONE)
                ref += '.'

        user = user and user.uid or '-'
        utype, provider, *_ = user.split('-')

        return functools.reduce(
            lambda acc, perm: (
                acc
                | perm.get('*', Permissions.NONE)
                | perm.get('{}-*'.format(utype), Permissions.NONE)
                | perm.get('{}-{}-*'.format(utype, provider), Permissions.NONE)
                | perm.get(user, Permissions.NONE)),
            (obj.permissions for obj in perm_objs),
            Permissions.NONE
        )
