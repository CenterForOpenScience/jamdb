from collections import namedtuple, OrderedDict
# from jam.models import fields
# from jam.models.base import Model


class DataObject(namedtuple('DataObject', ['ref', 'data'])):

    @classmethod
    def serialize(cls, inst):
        return inst._asdict()

    @classmethod
    def deserialize(cls, serial):
        # TODO Fix me
        serial.pop('_id', None)
        return cls(**serial)

    def _asdict(self):
        return OrderedDict(zip(self._fields, self))


# class DataObject(Model):
#     ref = fields.String()
#     data = fields.Raw()
