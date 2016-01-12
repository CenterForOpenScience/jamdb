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
  this.route('namespace', {path: '/n/:namespace_id'}, function() {
    this.route('collection', {path: '/c/:collection_id'}, function() {
        this.route('document', {path: '/d/:document_id'});
    });
  });
});

export default Router;
