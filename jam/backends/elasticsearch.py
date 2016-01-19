import operator
import functools
import logging

import elasticsearch_dsl
from elasticsearch import Elasticsearch

from jam import settings
from jam import exceptions
from jam.backends import query as queries
from jam.backends.base import Backend

logging.getLogger('elasticsearch').setLevel(logging.WARNING)


class ElasticsearchBackend(Backend):

    DEFAULT_CONNECTION = Elasticsearch(settings.ELASTICSEARCH_URI)

    ES_MAPPING = {'dynamic_templates': [{
        'inner_data': {
            'path_match': 'data.*',
            'match_mapping_type': 'string',
            'mapping': {
                'type': 'string',
                'fields': {
                    'raw': {'type': 'string', 'index': 'not_analyzed'}
                }
            }
        }
    }, {
        'top_level': {
            'match': '*',
            'match_mapping_type': 'string',
            'mapping': {'type': 'string', 'index': 'not_analyzed', 'include_in_all': False}
        },
    }]}

    # TODO (maybe) store as dates rather than timestamps
    # }, {
    #     'dates': {
    #         'match': '*',
    #         'match_mapping_type': 'double',
    #         'mapping': {'type': 'date', 'include_in_all': False}
    #     }

    @classmethod
    def settings_for(cls, namespace_id, collection_id, type_):
        return {
            'index': namespace_id,
            'doc_type': '{}-{}'.format(type_, collection_id),
        }

    def __init__(self, index, doc_type, connection=None):
        self._connection = connection or ElasticsearchBackend.DEFAULT_CONNECTION
        self._index = index
        self._doc_type = doc_type
        self._connection.indices.create(self._index, ignore=400)
        self._connection.indices.put_mapping(body={doc_type: self.ES_MAPPING}, index=index, doc_type=doc_type)
        self.search = elasticsearch_dsl.Search(self._connection, index=index, doc_type=doc_type)

    def get(self, key):
        assert not key.startswith('_'), 'Elasticsearch keys may not being with _'
        res = self._connection.get(index=self._index, doc_type=self._doc_type, id=key, ignore=404)

        if res.get('status') == 404 or not res['found']:
            raise exceptions.NotFound(key)

        return res['_source']

    def keys(self):
        return (x.meta['id'] for x in self.search.fields([]).execute().hits)

    def list(self, order=None):
        search = self.search
        if order:
            search = search.sort({
                order.key: {
                    'order': 'asc' if order.order > 0 else 'desc',
                    'unmapped_type': 'string'
                }
            })

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
        if isinstance(query, queries.CompoundQuery):
            return functools.reduce({
                queries.Or: operator.or_,
                queries.And: operator.and_
            }[query.__class__], [
                self._translate_query(q)
                for q in query.queries
            ])

        key = query.key
        if key.startswith('data.') and isinstance(query.value, str):
            key += '.raw'
        return elasticsearch_dsl.F({
            queries.Equal: 'term'
        }[query.__class__], **{key: query.value})
