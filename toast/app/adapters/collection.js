import Ember from 'ember';
import DS from 'ember-data';
import UrlTemplates from 'ember-data-url-templates';
import ENV from 'toast/config/environment';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';

// export default DS.JSONAPIAdapter.extend(DataAdapterMixin, UrlTemplates, {
export default DS.JSONAPIAdapter.extend(DataAdapterMixin, {
    authorizer: 'authorizer:jam-jwt',
    host: ENV.jamdbURL,
    namespace: 'v2',

    // _buildURL(modelName, id) {
    //   var url = [];
    //   var host = get(this, 'host');
    //   var prefix = this.urlPrefix();
    //   var path;

    //   if (modelName) {
    //     path = this.pathForType(modelName);
    //     if (path) { url.push(path); }
    //   }

    //   if (id) { url.push(encodeURI(id)); }
    //   if (prefix) { url.unshift(prefix); }

    //   url = url.join('/');
    //   if (!host && url && url.charAt(0) !== '/') {
    //     url = '/' + url;
    //   }

    //   return url;
    // }

    // adapterContext: Ember.inject.service(),
    // urlTemplate: '{+host}/v1/namespaces/{namespaceId}/collections{/id}',

    // urlSegments: {
    //     namespaceId(type, id, snapshot, query) {
    //         if (snapshot !== null && snapshot !== undefined && snapshot.record.get('namespace.id'))
    //           return snapshot.record.get('namespace.id');
    //         return this.get('adapterContext.namespace.id');
    //     }
    // }
});
