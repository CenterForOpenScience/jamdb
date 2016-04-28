import Ember from 'ember';
import DS from 'ember-data';


Ember.Inflector.inflector.uncountable('history');


export default DS.Model.extend({
    parameters: DS.attr(),
    recordId: DS.attr('string'),
    operation: DS.attr('string'),
    dateModified: DS.attr('date'),
    document: DS.belongsTo('document'),
});
