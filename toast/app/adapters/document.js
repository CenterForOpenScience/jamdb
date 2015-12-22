import DS from 'ember-data';
import UrlTemplates from 'ember-data-url-templates';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';

export default DS.JSONAPIAdapter.extend(DataAdapterMixin, UrlTemplates, {
    authorizer: 'authorizer:jam-jwt',
    host: 'http://localhost:1212',

    adapterContext: Ember.inject.service(),
    urlTemplate: '{+host}/v1/namespaces/{namespaceId}/collections{/collectionId}/documents{/id}',

    urlSegments: {
        collectionId(type, id, snapshot, query) {
            return this.get('adapterContext.collection.id');
        },
        namespaceId(type, id, snapshot, query) {
            return this.get('adapterContext.namespace.id');
        }
    }
});
