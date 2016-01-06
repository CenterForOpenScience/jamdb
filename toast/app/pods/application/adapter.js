import DS from 'ember-data';
import ENV from 'toast/config/environment';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';

export default DS.JSONAPIAdapter.extend(DataAdapterMixin, {
    authorizer: 'authorizer:jam-jwt',
    namespace: 'v1',
    host: ENV.jamdbURL
});
