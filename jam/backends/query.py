import abc


def get(dictionary, key):
    val = dictionary
    try:
        for k in key.split('.'):
            val = val[k]
    except KeyError:
        return None
    return val


# Base Classes
class BaseQuery(abc.ABC):

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    @abc.abstractmethod
    def as_lambda(self):
        raise NotImplementedError


class Query(BaseQuery, metaclass=abc.ABCMeta):

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    def __init__(self, field, value):
        self._key = field
        self._value = value

    def __repr__(self):
        return '<{}({}, {!r})>'.format(self.__class__.__name__, self.key, self.value)

    def __str__(self):
        return self.__repr__()


class CompoundQuery(BaseQuery, metaclass=abc.ABCMeta):

    @property
    def queries(self):
        return self._queries

    def __init__(self, *queries):
        self._queries = queries

    def __iter__(self):
        return self.queries

    def __repr__(self):
        return '<{}({})>'.format(
            self.__class__.__name__,
            ', '.join([q.__repr__() for q in self.queries])
        )

    def __str__(self):
        return self.__repr__()


# Compound queries
class And(CompoundQuery):

    def as_lambda(self):
        return lambda val: all(q.as_lambda()(val) for q in self.queries)

    def __and__(self, other):
        if not isinstance(other, CompoundQuery):
            return And(other, *self.queries)
        return super().__and__(other)


class Or(CompoundQuery):

    def as_lambda(self):
        return lambda val: any(q.as_lambda()(val) for q in self.queries)

    def __or__(self, other):
        if not isinstance(other, CompoundQuery):
            return Or(other, *self.queries)
        return super().__or__(other)


# Normal operators
class Equal(Query):

    def as_lambda(self):
        return lambda val: get(val, self.key) == self.value


class BitwiseAnd(Query):

    def as_lambda(self):
        return lambda val: bool(get(val, self.key) and (get(val, self.key) & self.value))


class BitwiseOr(Query):

    def as_lambda(self):
        return lambda val: bool(get(val, self.key) and (get(val, self.key) | self.value))


class In(Query):

    def as_lambda(self):
        return lambda val: get(val, self.key) in self.value


class NotEqual(Query):

    def as_lambda(self):
        return lambda val: get(val, self.key) != self.value


class LessThan(Query):

    def as_lambda(self):
        return lambda val: get(val, self.key) < self.value


class GreaterThan(Query):

    def as_lambda(self):
        return lambda val: get(val, self.key) > self.value


class GreaterThanOrEqualTo(Query):

    def as_lambda(self):
        return lambda val: get(val, self.key) >= self.value


class LessThanOrEqualTo(Query):

    def as_lambda(self):
        return lambda val: get(val, self.key) <= self.value


# API
def Q(key, operator, value):
    try:
        return {
            'in': In,
            'eq': Equal,
            'ne': NotEqual,
            'lt': LessThan,
            'or': BitwiseOr,
            'and': BitwiseAnd,
            'gt': GreaterThan,
            'lte': LessThanOrEqualTo,
            'gte': GreaterThanOrEqualTo,
        }[operator](key, value)
    except KeyError:
        raise ValueError('Unsupported operator {}'.format(operator))
