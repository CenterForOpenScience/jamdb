import abc


class ReadOnlyBackend(abc.ABC):

    @abc.abstractmethod
    def get(self, key):
        raise NotImplementedError

    @abc.abstractmethod
    def keys(self):
        raise NotImplementedError

    def query(self, query, order=None):
        return filter(query.as_lambda(), self.list(order))

    def first(self, query):
        return next(self.query(query))

    def list(self, order=None):
        order = order or (lambda x: x)
        return order(self.get(key) for key in self.keys())


class Backend(ReadOnlyBackend):

    @abc.abstractmethod
    def set(self, key, value):
        raise NotImplementedError

    @abc.abstractmethod
    def unset(self, key):
        raise NotImplementedError

    @abc.abstractmethod
    def unset_all(self):
        raise NotImplementedError
