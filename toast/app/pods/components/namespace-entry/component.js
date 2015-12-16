import Ember from 'ember';

const Component = Ember.Component.extend({
    showCollections: false,

    tagName: 'li',
    classNames: ['treeview'],
    classNameBindings: ['showCollections:active'],
    actions: {
        toggle() {
            this.set('showCollections', !this.get('showCollections'));
        }
    }
});

Component.reopenClass({
    positionalParams: ['namespace']
});

export default Component;
