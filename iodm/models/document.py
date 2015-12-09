from collections import namedtuple

from iodm.auth import Permissions


class Document(namedtuple('Document', [
    'ref',  # record id
    'log_ref',

    'data',  # nullable if data_ref is defined
    'data_ref',  # nullable if date is defined

    # TODO required for permissions?
    'created_by',
    'created_on',
    'modified_by',
    'modified_on',
])):

    @classmethod
    def create(cls, log, data):
        return cls(
            ref=log.record_id,
            log_ref=log.ref,
            data=data,
            data_ref=log.data_ref,
            created_by=log.created_by,
            created_on=log.created_on,
            modified_by=log.modified_by,
            modified_on=log.modified_on,
        )

    @classmethod
    def serialize(cls, inst):
        return inst._asdict()

    @classmethod
    def deserialize(cls, serial):
        serial.pop('_id', None)
        return cls(**serial)

    def __new__(cls, **kwargs):
        kwargs['created_on'] = float(kwargs['created_on'])
        kwargs['modified_on'] = float(kwargs['modified_on'])
        return super().__new__(cls, **kwargs)

    @property
    def permissions(self):
        return {self.created_by: Permissions.CRUD}

    def to_json_api(self):
        return {
            'id': self.ref,
            'type': 'document',
            'attributes': self.data,
            'meta': {
                'created-by': self.created_by,
                'created-on': self.created_on,
                'modified-by': self.modified_by,
                'modified-on': self.modified_on,
            }
        }
