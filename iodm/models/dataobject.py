from collections import namedtuple


class DataObject(namedtuple('DataObject', ['ref', 'data'])):

    @classmethod
    def serialize(cls, inst):
        return inst._asdict()

    @classmethod
    def deserialize(cls, serial):
        serial.pop('_id', None)
        return cls(**serial)
