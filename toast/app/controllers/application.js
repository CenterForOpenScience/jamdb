import Ember from 'ember';

export default Ember.Controller.extend({
    queryParams: {'skinParam': 'skin'},
    skin: Ember.computed('skinParam', function() {
        return 'skin-' + (this.skinParam || 'black');
    }),

});
