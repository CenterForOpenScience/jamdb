import Ember from 'ember';


export default Ember.Mixin.create({
    size: 'md',
    classNameBindings: ['_size'],
    _size: Ember.computed('_classType', function() {
        return this.get('_classType')  + '-' + this.get('size');
    })
});
