import Ember from 'ember';
import ENV from 'toast/config/environment';

export default Ember.Component.extend({
  windowHash: function() {
    return window.location.hash
      .substring(1)
      .split('&')
      .map(function(str) {return this[str.split('=')[0]] = str.split('=')[1], this;}.bind({}))[0];
  }.property(),
  didInitAttrs() {
    this._super(...arguments);
    if (!this.get('hash.access_token')) return;
    window.location.hash = '';
    this.get('login')({
      provider: 'osf',
      access_token: this.get('hash.access_token')
    });
  },
  actions: {
    authenticate() {
      window.location = `${ENV.auth.osf.url}/oauth2/authorize?response_type=token&scope=${ENV.auth.osf.scope}&client_id=${ENV.auth.osf.clientId}&redirect_uri=${encodeURIComponent(window.location)}`;
    }
  }
});

