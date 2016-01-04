import operator

from stevedore import driver


def get_backend(name):
    return driver.DriverManager('jam.backends', name).driver


def load_backend(name, *args, **kwargs):
    return driver.DriverManager(
        'jam.backends',
        name,
        invoke_on_load=True,
        invoke_args=args,
        invoke_kwds=kwargs,
    ).driver


class QueryCommand:

    def __init__(self, backend, _fields=None, _query=None, _limit=None, _skip=None, _order_by=None):
        assert not _fields, 'Field selection is not currently supported'
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
            rep.append('OrderBy({!r})'.format(self._order_by))
        if self._limit:
            rep.append('Limit({})'.format(self._limit))
        if self._skip:
            rep.append('Skip({})'.format(self._skip))
        return '.'.join(rep)
