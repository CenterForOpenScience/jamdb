import operator
import functools

import elasticsearch_dsl
from elasticsearch import Elasticsearch

from iodm import exceptions
from iodm.backends.base import Backend
from iodm.backends.util import CompoundQuery


class ElasticsearchBackend(Backend):

    DEFAULT_CONNECTION = Elasticsearch()

    @classmethod
    def settings_for(cls, namespace_id, collection_id, type_):
        return {
            'index': namespace_id,
            'doc_type': '{}-{}'.format(collection_id, type_),
        }

    def __init__(self, index, doc_type, connection=None):
        self._connection = connection or ElasticsearchBackend.DEFAULT_CONNECTION
        self._index = index
        self._doc_type = doc_type
        self._connection.indices.create(self._index, ignore=400)
        m = elasticsearch_dsl.Mapping(doc_type)
        m.field('ref', 'string', index='not_analyzed')
        self._connection.indices.put_mapping(body=m.to_dict(), index=index, doc_type=doc_type)
        self.search = elasticsearch_dsl.Search(self._connection, index=index, doc_type=doc_type)

    def get(self, key):
        res = self._connection.get(index=self._index, doc_type=self._doc_type, id=key, ignore=404)

        if res.get('status') == 404 or not res['found']:
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

    def query(self, query, order=None, limit=None, skip=None):
        search = self.search
        if order:
            search = search.sort({
                order.key: 'asc' if order.order > 0 else 'desc'
            })

        search = search[skip or 0:(limit or 100) + (skip or 0)]
        if query:
            search = search.filter(self._translate_query(query))

        return (hit['_source'] for hit in search.execute().hits.hits)

    def count(self, query):
        search = self.search
        if query:
            search = search.filter(self._translate_query(query))
        return search.execute().hits.total

    def unset_all(self):
        self._connection.delete_by_query(index=self._index, doc_type=self._doc_type, body={
            'query': {
                'match_all': {}
            }
        })

    def _translate_query(self, query):
        if isinstance(query, CompoundQuery):
            return functools.reduce(operator.and_, [
                self._translate_query(q)
                for q in query.queries
            ])
        return elasticsearch_dsl.F({
            'eq': 'term'
        }[query.comparator], **{query.key: query.value})
