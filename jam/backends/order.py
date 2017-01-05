import abc


def get(dictionary, key):
    val = dictionary
    try:
        for k in key.split('.'):
            val = val[k]
    except KeyError:
        return 0  # 0 is sortable...
    return val


class Order(abc.ABC):
    ASCENDING = 1
    DESCENDING = -1

    def __init__(self, key, order):
        assert order in (-1, 1)
        self.key = key
        self.order = order

    def __call__(self, iterable):
        return sorted(iterable, key=lambda x: get(x, self.key), reverse=bool(self.order < 0))

    def __repr__(self):
        return '<{}({})>'.format(self.__class__.__name__, self.key)


class Ascending(Order):

    def __init__(self, key):
        super().__init__(key, Order.ASCENDING)


class Descending(Order):

    def __init__(self, key):
        super().__init__(key, Order.DESCENDING)


# API
def O(key, order):
    try:
        return {
            1: Ascending,
            -1: Descending
        }[order](key)
    except KeyError:
        raise ValueError('Unsupported order {}'.format(order))


O.Ascending = Ascending
O.Descending = Descending
O.ASCENDING = Order.ASCENDING
O.DESCENDING = Order.DESCENDING
