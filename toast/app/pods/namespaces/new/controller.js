import Ember from 'ember';


export default Ember.Controller.extend({
    session: Ember.inject.service('session'),

    name: null,

    actions: {
        create() {
            this.store.createRecord('namespace', {
                'name': this.get('name'),
                'perimissions': {
                    [this.get('store.uid')]: 9223372036854776000
                }
            }).save();
        }
    }
});
