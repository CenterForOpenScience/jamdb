import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {
    model(params) {
        return this.modelFor('namespace').query('collections', {id: params.collection_id});
    },
    setupController(controller, model) {
        this._super(controller, model);
        controller.set('isLoading', true);
        model.get('documents', {limit: 10, offset: 0}).then(function(docs) {
            controller.set('isLoading', false);
            controller.set('isEmpty', docs.length === 0);
            controller.set('attributes', docs.get('firstObject.attributeNames'));
        });
    }
});
