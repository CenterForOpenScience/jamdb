import Ember from 'ember';

export default Ember.Controller.extend({
  session: Ember.inject.service('session'),
  queryParams: ['driver'],
  authDrivers: ['Jam', 'OSF'],
  driver: 'jam-auth',

  actions: {
    selectAuthMethod(method) {
      this.set('driver', `${method.toLowerCase()}-auth`);
    },
    authenticate(attrs) {
      this.store.unloadAll('namespace');
      this.get('session').authenticate('authenticator:jam-jwt', attrs);
    }
  }
});
