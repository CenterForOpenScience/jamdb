import Ember from 'ember';

const Component = Ember.Component.extend({
  store: Ember.inject.service(),
  routing: Ember.inject.service('-routing'),

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
        id: [this.get('namespace.id'), name].join('.'),
        namespace: this.get('namespace')
      }).save().then(() => this.toggleProperty('isCreating'));
    }
  },

  init() {
    this._super.apply(this, arguments);

    // Hack to force the current namespace open
    let params = this.get('routing.targetState.routerJsState.params')[this.get('routing.currentRouteName')];
    if (Object.keys(params).length > 0 && params[Object.keys(params)[0]].split('.')[0] === this.namespace.id)
      this.set('showCollections', true);
  }
});

Component.reopenClass({
  positionalParams: ['namespace']
});

export default Component;
