import enum
import collections
from marshmallow import Schema, fields


class DataObjectSchema(Schema):
    ref = fields.String()
    data = fields.Raw()


DataObject = collections.namedtuple('DataObject', [
    'ref',
    'data'
])


class LogSchema(Schema):
    ref = fields.String()
    version = fields.String()
    data_ref = fields.String(allow_none=True)
    operation = fields.Integer()
    record_id = fields.String(allow_none=True)
    timestamp = fields.Float()
    operation_parameters = fields.Dict(default=dict, missing=dict)


Log = collections.namedtuple('Log', [
    'ref',
    'version',
    'data_ref',
    'operation',
    'record_id',
    'timestamp',
    'operation_parameters',
])


class Operation(enum.IntEnum):
    CREATE = 0
    UPDATE = 1
    REPLACE = 2
    DELETE = 3
    SNAPSHOT = 4
    RENAME = 5
