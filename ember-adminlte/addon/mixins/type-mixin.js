import Ember from 'ember';


export default Ember.Mixin.create({
    type: 'default',
    _classType: null,
    classNameBindings: ['typeClass'],
    typeClass: Ember.computed(function() {
        return this.get('_classType') + ' ' + this.get('_classType') + '-' + this.get('type');
    })
});
