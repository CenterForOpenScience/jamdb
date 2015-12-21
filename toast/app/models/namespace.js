import DS from 'ember-data';

export default DS.Model.extend({
    permissions: DS.attr(),
    name: DS.attr('string'),
    state: DS.attr('string'),
    logger: DS.attr('string'),
    storage: DS.attr('string'),
    createdOn: DS.attr('date'),
    collections: DS.hasMany('collection', {async: true}),
});
