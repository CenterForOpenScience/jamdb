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
      this.get('session').authenticate('authenticator:jam-jwt', attrs).then(() => {
        this.set('model', this.store.findAll('namespace'));
      });
    }
  }
});
