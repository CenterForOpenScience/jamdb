import Ember from 'ember';

export default Ember.Controller.extend({
    session: Ember.inject.service('session'),

    queryParams: {'skinParam': 'skin'},
    skin: Ember.computed('skinParam', function() {
        return 'skin-' + (this.skinParam || 'black');
    }),

});
