import DS from 'ember-data';
import HasManyQuery from 'ember-data-has-many-query';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';

export default DS.JSONAPIAdapter.extend(DataAdapterMixin, HasManyQuery.RESTAdapterMixin, {
    authorizer: 'authorizer:jam-jwt',
    namespace: 'v1',
    host: 'http://localhost:1212'
});
