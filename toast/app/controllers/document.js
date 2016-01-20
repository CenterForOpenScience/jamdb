import Ember from 'ember';

const OPromise = Ember.ObjectProxy.extend(Ember.PromiseProxyMixin);

export default Ember.Controller.extend({
  history: OPromise.create(),

  page: 1,
  queryParams: ['page'],

  _init: function() {
    this.set('history', this.store.query('history', {
      'document': this.get('model'),
      'page[Size]': this.get('size')
    }));
  }.observes('model')
});
