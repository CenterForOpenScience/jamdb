import DS from 'ember-data';
import Ember from 'ember';

export default DS.Model.extend({
    collection: DS.belongsTo('collection'),
    attributes: DS.attr(),
    createdOn: DS.attr('date'),
    createdBy: DS.attr('string'),
    modifiedOn: DS.attr('date'),
    modifiedBy: DS.attr('string'),
    history: DS.hasMany('history', {async: true})
});
