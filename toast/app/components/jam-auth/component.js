import Ember from 'ember';
import ENV from 'toast/config/environment';

export default Ember.Component.extend({
  namespace: ENV.auth.self.defaultNamespace,
  collection: ENV.auth.self.defaultCollection,

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

