import DS from 'ember-data';
import Ember from 'ember';

export default DS.Model.extend({
    collection: DS.belongsTo('collection'),
    attributes: DS.attr(),
    createdOn: DS.attr('date'),
    createdBy: DS.attr('string'),
    ModifiedOn: DS.attr('date'),
    ModifiedBy: DS.attr('string'),
    attributeNames: Ember.computed('attributes', function() {
        return Object.keys(this.get('attributes'));
    }),
});
