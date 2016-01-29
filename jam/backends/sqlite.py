import operator
import functools
import peewee
from playhouse import sqlite_ext

from jam import settings
from jam import exceptions
from jam.backends import query as queries
from jam.backends.base import Backend
from jam.backends.util import QueryCommand


class Log(peewee.Model):
    class Meta:
        table_alias = 'log'

    ref = peewee.CharField(primary_key=True)
    data_ref = peewee.CharField()
    record_id = peewee.CharField()
    version = peewee.CharField()

    operation = peewee.CharField()
    operation_parameters = sqlite_ext.JSONField()

    created_by = peewee.CharField()
    created_on = peewee.IntegerField()
    modified_by = peewee.CharField()
    modified_on = peewee.IntegerField()


class DataObject(peewee.Model):
    class Meta:
        table_alias = 'dataobject'

    ref = peewee.CharField(primary_key=True)
    data = sqlite_ext.JSONField()


class Document(peewee.Model):
    class Meta:
        table_alias = 'document'

    ref = peewee.CharField(primary_key=True)

    log_ref = peewee.CharField()

    data_ref = peewee.CharField()
    data = sqlite_ext.JSONField()

    created_by = peewee.CharField()
    created_on = peewee.IntegerField()
    modified_by = peewee.CharField()
    modified_on = peewee.IntegerField()


class SQLiteBackend(Backend):

    DEFAULT_CONNECTION = peewee.SqliteDatabase(settings.SQLITE_URI)
    MODEL_MAP = {
        'logger': Log,
        'state': Document,
        'storage': DataObject
    }

    @classmethod
    def settings_for(cls, namespace_id, collection_id, type_):
        return {
            'table': '{}-{}-{}'.format(type_, namespace_id, collection_id)
        }

    def __init__(self, table, connection=None):
        self._connection = connection or SQLiteBackend.DEFAULT_CONNECTION
        self._model = self.MODEL_MAP[table.split('-')[0]]
        self._model._meta.db_table = table
        self._model._meta.database = self._connection

        self._connection.connect()
        self._connection.create_table(self._model, True)

    def get(self, key):
        try:
            return self._model.get(ref=key)._data
        except self._model.DoesNotExist:
            raise exceptions.NotFound(key)

    def keys(self):
        for val in self._model.select(self._model.ref):
            yield val.ref

    def list(self, order=None):
        sel = self._model.select()
        if order:
            sel.order_by(self._translate_order(order))
        return iter(sel)

    def set(self, key, data):
        self._model.create(**data)

    def unset(self, key):
        self.get(key).delete_instance()

    def query(self, query, order=None, limit=None, skip=None):
        sel = self._model.select()
        if order:
            sel.order_by(self._translate_order(order))
        if query:
            import ipdb; ipdb.set_trace()
            sel = sel.where(self._translate_query(query))
        if limit is not None:
            sel = sel.limit(limit)
        if skip is not None:
            sel = sel.offset(skip)
        return iter(sel)

    def count(self, query):
        sel = self._model.select()
        if query:
            sel = sel.where(self._translate_query(query))
        return sel.count()

    def unset_all(self):
        self._model.delete().execute()

    def _translate_query(self, query):
        if isinstance(query, queries.CompoundQuery):
            return functools.reduce({
                queries.Or: operator.or_,
                queries.And: operator.and_,
            }[query.__class__], [
                self._translate_query(q)
                for q in query.queries
            ])

        if '.' in query.key:
            name, *tail = query.key.split('.')
            import ipdb; ipdb.set_trace()
            field = getattr(self._model, name)(path='.'.join(tail))
        else:
            field = getattr(self._model, query.key)
        return {
            queries.In: operator.contains,
            queries.Equal: operator.eq,
            queries.NotEqual: operator.ne,
        }[query.__class__](field, query.value)

    def _translate_order(self, order):
        field = getattr(self._model, order.key)
        if order == order.ASCENDING:
            return +field
        return - field
