import DS from 'ember-data';
import ENV from 'toast/config/environment';
import UrlTemplates from 'ember-data-url-templates';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';

export default DS.JSONAPIAdapter.extend(DataAdapterMixin, UrlTemplates, {
    authorizer: 'authorizer:jam-jwt',
    host: ENV.jamdbURL,
    namespace: 'v2',

    queryUrlTemplate: '{+host}/v2/documents{/documentId}/history',

    urlSegments: {
        documentId(type, id, snapshot, query) {
          let dId = query.document.id;
          delete query.document;
          return dId;
        }
    }
});
