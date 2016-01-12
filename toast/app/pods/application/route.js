import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin, {
  model(params) {
    return this.store.findAll('namespace');
  },
  actions: {
    error(reason) {
      this.transitionTo('error');
      console.log(reason);
    }
  }
});
