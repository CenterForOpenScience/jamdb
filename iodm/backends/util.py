import operator


def get(dictionary, key):
    val = dictionary
    for k in key.split('.'):
        val = val[k]
    return val


class Query:

    SUPPORTED_COMPARATORS = ('eq', 'ne', 'in', 'gt', 'lt', 'lte', 'gte')

    def __init__(self, key, comparator, value):
        assert comparator in self.SUPPORTED_COMPARATORS
        self.key = key
        self.value = value
        self.comparator = comparator

    def as_lambda(self):
        comparator = getattr(operator, {
            'gte': 'ge',
            'lte': 'le',
        }.get(self.comparator, self.comparator))
        return lambda val: comparator(get(val, self.key), self.value)

    def __and__(self, other):
        return CompoundQuery(self, other)


class CompoundQuery:

    def __init__(self, *queries):
        self.queries = queries

    def as_lambda(self):
        return lambda val: all(q.as_lambda()(val) for q in self.queries)


class Order:
    ASCENDING = 1
    DESCENDING = -1

    @classmethod
    def Ascending(cls, key):
        return cls(key, cls.ASCENDING)

    @classmethod
    def Descending(cls, key):
        return cls(key, cls.DESCENDING)

    def __init__(self, key, order):
        assert order in (-1, 1)
        self.key = key
        self.order = order

    def __call__(self, iterable):
        return sorted(iterable, key=lambda x: get(x, self.key), reverse=bool(self.order < 0))


class QueryCommand:

    def __init__(self, backend, _fields=None, _query=None, _limit=None, _skip=None, _order_by=None):
        assert not _fields, 'Field selection is currenly unsupported'
        self.backend = backend

        self._skip = _skip
        self._limit = _limit
        self._query = _query
        self._fields = _fields
        self._order_by = _order_by

    def __iter__(self):
        return self.execute()

    def where(self, query):
        return QueryCommand(**{**self.__dict__, '_query': query})

    def order_by(self, order_by):
        return QueryCommand(**{**self.__dict__, '_order_by': order_by})

    def limit(self, limit):
        return QueryCommand(**{**self.__dict__, '_limit': limit})

    def skip(self, skip):
        return QueryCommand(**{**self.__dict__, '_skip': skip})

    def page(self, page, page_size):
        # Note: pages are base 0
        return QueryCommand(**{**self.__dict__, '_limit': page_size, '_skip': page * page_size})

    def count(self):
        return self.backend.count(self._query)

    def execute(self):
        return self.backend._exec_query(self)

    def __repr__(self):
        rep = ['Select(*)']
        if self._query:
            rep.append('Where({!r})'.format(self._query))
        if self._order_by:
            rep.append('OrderBy({!r})'.format(self._order_by._name))
        if self._limit:
            rep.append('Limit({})'.format(self._limit))
        if self._skip:
            rep.append('Skip({})'.format(self._skip))
        return '.'.join(rep)
