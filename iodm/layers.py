import abc


class Layer(abc.ABC):
    pass


class CreationLayer(Layer):

    def set(self, *args, **kwargs):
        key, obj = self.create(*args, **kwargs)
        super().set(key, obj)
        return obj


class NameTupleLayer(Layer):

    def __init__(self, named):
        self.named = named
        super().__init__()

    def get(self, key):
        return self.named(**super().get(key))

    def set(self, key, named):
        return super().set(key, named._asdict())
