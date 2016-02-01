import DS from 'ember-data';
import ENV from 'toast/config/environment';
import UrlTemplates from 'ember-data-url-templates';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';

export default DS.JSONAPIAdapter.extend(DataAdapterMixin, UrlTemplates, {
    authorizer: 'authorizer:jam-jwt',
    host: ENV.jamdbURL,
    namespace: 'v1/id',

    queryUrlTemplate: '{+host}/v2/collections{/collectionId}/_search',

    urlSegments: {
        collectionId(type, id, snapshot, query) {
          let collectionId = query.collection.id;
          delete query.collection;
          return collectionId;
        }
    }
});
