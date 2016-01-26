import Ember from 'ember';

const Component = Ember.Component.extend({
  store: Ember.inject.service(),
  classNames: ['box'],
});

Component.reopenClass({
  positionalParams: ['collection']
});

export default Component;
