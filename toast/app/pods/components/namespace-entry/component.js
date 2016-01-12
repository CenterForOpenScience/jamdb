import Ember from 'ember';

const Component = Ember.Component.extend({
  store: Ember.inject.service(),
  adapterContext: Ember.inject.service(),

  tagName: 'li',
  isCreating: false,
  showCollections: false,
  classNames: ['treeview'],
  classNameBindings: ['showCollections:active'],

  actions: {
    toggle() {
      this.toggleProperty('showCollections');
    },
    toggleCreation() {
      this.toggleProperty('isCreating');
      if (this.get('isCreating'))
        this.$('input[type=text]').focus();
    },
    newCollection(name) {
      this.get('store').createRecord('collection', {
          id: name,
          namespace: this.get('namespace')
      }).save();
      this.toggleProperty('isCreating');
    }
  },

  init() {
    this._super.apply(this, arguments);
    if (this.get('adapterContext.namespace.id') == this.namespace.id)
      this.set('showCollections', true);
  }
});

Component.reopenClass({
  positionalParams: ['namespace']
});

export default Component;
