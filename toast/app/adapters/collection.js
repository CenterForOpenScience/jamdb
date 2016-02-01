import DS from 'ember-data';
import ENV from 'toast/config/environment';
import UrlTemplates from 'ember-data-url-templates';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';

export default DS.JSONAPIAdapter.extend(DataAdapterMixin, UrlTemplates, {
    authorizer: 'authorizer:jam-jwt',
    host: ENV.jamdbURL,
    namespace: 'v1/id',

    createRecordUrlTemplate: '{+host}/v2/namespaces{/namespaceId}/collections',

    urlSegments: {
      namespaceId(type, id, snapshot) {
        return snapshot.record.get('namespace.id');
      }
    }
});
