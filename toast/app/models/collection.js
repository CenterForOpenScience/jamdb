import DS from 'ember-data';

export default DS.Model.extend({
    name: function() {
      return this.get('id').split('.')[1];
    }.property(),
    permissions: DS.attr(),
    documents: DS.hasMany('document', {async: true}),
    namespace: DS.belongsTo('namespace'),
});
