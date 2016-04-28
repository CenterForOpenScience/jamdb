import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('login');
  this.route('error', {path: '/oops'});
  this.route('document', {path: '/d/:document_id'});
  this.route('namespace', {path: '/n/:namespace_id'});
  this.route('collection', {path: '/c/:collection_id'});
  this.route('document-edit', {path: '/d/:document_id/edit'});
});

export default Router;
