from iodm.backends import Order


class Field:

    @property
    def Ascending(self):
        return (self._name, Order.ASCENDING)

    @property
    def Descending(self):
        return (self._name, Order.ASCENDING)

    def serialize(self, value):
        raise NotImplementedError

    def deserialize(self, value):
        raise NotImplementedError

    def __and__(self, value):
        pass
        # return query.BitwiseAnd(self, value)

    def __or__(self, value):
        pass
        # return query.BitwiseOr(self, value)

    def __eq__(self, value):
        return Query.Equals(self, value)

    def __ne__(self, value):
        pass

    def __lt__(self, value):
        pass

    def __gt__(self, value):
        pass

    def __ge__(self, value):
        pass

    def __le__(self, value):
        pass


class Raw(Field):
    pass


class String(Field):
    pass
