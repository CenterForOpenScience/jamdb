import Ember from 'ember';
import DS from 'ember-data';
import HasManyQuery from 'ember-data-has-many-query';


Ember.Inflector.inflector.uncountable('history');


export default DS.Model.extend(HasManyQuery.ModelMixin, {
    parameters: DS.attr(),
    recordId: DS.attr('string'),
    operation: DS.attr('string'),
    document: DS.belongsTo('document'),
});
