import Ember from 'ember';


export default Ember.Component.extend({
    tagName: 'nav',
    role: 'navigation',
    attributeBindings: ['role'],
    classNames: ['navbar', 'navbar-static-top'],
});
