import Em from 'ember';
import DS from 'ember-data';

export default DS.Model.extend({
    name: Em.computed.alias('id'),
    // name: DS.attr('string'),
    permissions: DS.attr(),
    createdOn: DS.attr('date'),
    documents: DS.hasMany('document', {async: true}),
    namespace: DS.belongsTo('namespace'),
});
