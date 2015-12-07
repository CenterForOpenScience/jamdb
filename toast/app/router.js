import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('login');
  this.route('namespaces', function() {
      this.route('new');
  });
  this.route('namespace', {path: '/namespace/:namespace_id'}, function() {
    this.route('collection', {path: '/collection/:collection_id'});
  });
});

export default Router;
