import Ember from 'ember';

export default Ember.Component.extend({
  namespace: 'SHARE',
  collection: 'users',

  username: null,
  password: null,

  actions: {
    authenticate() {
      this.get('login')({
        provider: 'self',
        namespace: this.get('namespace'),
        collection: this.get('collection'),
        username: this.get('username'),
        password: this.get('password')
      });
      return false;
    }
  }
});

