import sys
import enum
import functools


class Permissions(enum.IntEnum):
    NONE = 0x0

    CREATE = 0x1
    READ = 0x1 << 1
    UPDATE = 0x1 << 2
    DELETE = 0x1 << 3

    C = CREATE
    CR = C | READ
    CRU = CR | UPDATE
    CRUD = CRU | DELETE

    RU = READ | UPDATE
    RUD = RU | DELETE

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
    def get_permissions(cls, user, *perm_objs):
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
