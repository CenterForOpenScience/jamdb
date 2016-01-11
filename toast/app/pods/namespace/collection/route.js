import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {
    adapterContext: Ember.inject.service(),

    model(params) {
        this.set('adapterContext.namespace', this.modelFor('namespace'));
        return this.store.findRecord('collection', params.collection_id);
    },
    setupController: function(controller, model) {
      this.set('adapterContext.collection', model);
      return this._super.apply(this, arguments);
    }
});
