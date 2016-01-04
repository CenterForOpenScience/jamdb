from jam.models.fields import Field


class ModelMeta(type):

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        cls._fields = {}
        for key, value in cls.__dict__.items():
            if not isinstance(value, Field):
                continue

            value.name = key
            cls._fields[key] = value


class Model(metaclass=ModelMeta):

    @classmethod
    def serialize(cls, inst):
        return {
            field.serialize(getattr(inst, field.name))
            for field in cls._fields.values()
        }

    @classmethod
    def deserialize(cls, partial, serialized):
        return cls(partial, **serialized)

    def __init__(self, **attrs):
        for field in self.__class__._fields.values():
            setattr(field.name, field.deserialize(attrs[field.name]))
