from collections import namedtuple
# from iodm.models import fields
# from iodm.models.base import Model


class DataObject(namedtuple('DataObject', ['ref', 'data'])):

    @classmethod
    def serialize(cls, inst):
        return inst._asdict()

    @classmethod
    def deserialize(cls, serial):
        # TODO Fix me
        serial.pop('_id', None)
        return cls(**serial)


# class DataObject(Model):
#     ref = fields.String()
#     data = fields.Raw()
