import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {
    model(params) {
        return this
            .modelFor('namespace')
            .get('collections')
            .then((collections) =>
                    collections.find((el) =>
                        el.id == params.collection_id
                )
            );
    },
    setupController(controller, model) {
        this._super(controller, model);
        model.get('documents').then(function(docs) {
            controller.set('isLoading', false);
            controller.set('isEmpty', docs.length === 0);
            // controller.set('attributes', docs.get('firstObject.attributeNams'));
            controller.set('attributes', docs.get('firstObject.attributeNames'));
        });
    }
});
