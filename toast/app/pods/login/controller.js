import Ember from 'ember';

export default Ember.Controller.extend({
    session: Ember.inject.service('session'),

    username: null,
    password: null,

    actions: {
        authenticate() {
            this.get('session').authenticate('authenticator:jam-namespace-jwt', 'SHARE', this.get('username'), this.get('password'));
            this.store.findAll('namespace');
        }
    }
});
