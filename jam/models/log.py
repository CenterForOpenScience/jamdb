from collections import namedtuple, OrderedDict

from jam.base import Operation


class Log(namedtuple('Log', [
    'ref',  # PK
    'data_ref',  # nullable
    'record_id',  # nullable

    'version',

    'operation',
    'operation_parameters',  # default empty dict

    # TODO required for permissions?
    'created_by',
    'created_on',
    'modified_by',
    'modified_on',
])):

    @classmethod
    def serialize(cls, inst):
        ret = inst._asdict()
        ret['operation'] = int(ret['operation'])
        return ret

    @classmethod
    def deserialize(cls, serial):
        serial.pop('_id', None)
        return cls(**serial)

    def __new__(cls, **kwargs):
        kwargs['operation'] = Operation(kwargs['operation'])
        kwargs['created_on'] = float(kwargs['created_on'])
        kwargs['modified_on'] = float(kwargs['modified_on'])
        kwargs.setdefault('operation_parameters', {})
        return super().__new__(cls, **kwargs)

    def _asdict(self):
        return OrderedDict(zip(self._fields, self))
