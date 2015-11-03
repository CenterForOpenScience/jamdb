import operator


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
        return lambda val: comparator(val[self.key], self.value)

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

    def __init__(self, key, order):
        assert order in (-1, 1)
        self.key = key
        self.order = order

    def __call__(self, iterable):
        return sorted(iterable, key=lambda x: x[self.key], reverse=bool(self.order < 0))
