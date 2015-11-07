import functools

import elasticsearch_dsl
from elasticsearch import Elasticsearch

from iodm import exceptions
from iodm.backends.base import Backend
from iodm.backends.util import CompoundQuery


class ElasticsearchBackend(Backend):

    DEFAULT_CONNECTION = Elasticsearch()

    def __init__(self, index, doc_type, connection=None):
        self._connection = connection or ElasticsearchBackend.DEFAULT_CONNECTION
        self._index = index
        self._doc_type = doc_type
        self.search = elasticsearch_dsl.Search(self._connection, index=index, doc_type=doc_type)

    def get(self, key):
        res = self._connection.get(index=self._index, doc_type=self._doc_type, id=key, ignore=404)

        if not res['found']:
            raise exceptions.NotFound(key)

        return res['_source']

    def keys(self):
        return (x.meta['id'] for x in self.search.fields([]).execute().hits)

    def list(self, order=None):
        search = self.search
        if order:
            search = search.order(str(order.order).replace('1', '') + order.key)

        resp = search.execute()
        from_, size, total = 0, 10, resp.hits.total
        while from_ * size < total:
            for hit in resp.hits.hits:
                yield hit['_source']
            from_ += len(resp.hits)
            resp = search[from_:from_+size].execute()

    def set(self, key, data):
        self._connection.index(index=self._index, doc_type=self._doc_type, id=key, body=data)

    def unset(self, key):
        self._connection.delete(index=self._index, doc_type=self._doc_type, id=key)

    def query(self, query, order=None):
        search = self.search
        if order:
            search = search.order(str(order.order).replace('1', '') + order.key)

        if isinstance(query, CompoundQuery):
            search = search.filter(
                functools.reduce(lambda a, b: a & b, [
                    elasticsearch_dsl.F(q.comparator, **{q.key: q.value})
                    for q in query.queries
                ])
            )
        else:
            search = search.filter(elasticsearch_dsl.F(q.comparator, **{q.key: q.value}))

        import ipdb; ipdb.set_trace()
        return (hit['_source'] for hit in search.execute().hits.hits)

    def unset_all(self):
        self._connection.delete_by_query(index=self._index, doc_type=self._doc_type, body={
            'query': {
                'match_all': {}
            }
        })
