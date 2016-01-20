import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin, {
  model() {
    return this.store.findAll('namespace');
  },
  actions: {
    error(reason) {
      this.transitionTo('error');
      console.log(reason);
    }
  }
});
