import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {
    adapterContext: Ember.inject.service(),

    model(params) {
        let self = this;
        this.set('adapterContext.namespace', this.modelFor('namespace'));
        this.set('adapterContext.collection', this.modelFor('namespace.collection'));
        return this.store.find('document', params.document_id);
    }
});
