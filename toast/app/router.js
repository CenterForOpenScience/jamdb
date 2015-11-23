import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('login');
  this.route('namespaces', function() {
      this.route('index', {path: '/:namespace_id'});
  });
});

export default Router;
