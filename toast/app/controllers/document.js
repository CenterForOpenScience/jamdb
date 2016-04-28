import Ember from 'ember';
import {objectToJsTree} from './collection';

const OPromise = Ember.ObjectProxy.extend(Ember.PromiseProxyMixin);

export default Ember.Controller.extend({
  history: OPromise.create(),

  page: 1,
  queryParams: ['page'],

  _init: function() {
    this.set('history', this.store.query('history', {
      'sort': '-modified_on',
      'document': this.get('model'),
      'page[size]': this.get('size'),
    }));
  }.observes('model'),

  tableData: function() {
    return this.get('history').map(el =>
      objectToJsTree({
        [el.get('id')]: el.get('data')
    })[0]);
  }.property('history')
});
