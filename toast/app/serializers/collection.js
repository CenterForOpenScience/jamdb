import DS from 'ember-data';

const READONLY = ['created-on', 'modified-on', 'created-by', 'modified-by'];

export default DS.JSONAPISerializer.extend({
  serialize(snapshot, options) {
    let serialized = this._super(...arguments);
    //EmberData still lacks support for readonly...
    READONLY.forEach(key => delete serialized.data.attributes[key]);
    //Relationships are implied via the URI
    delete serialized.data.relationships;
    return serialized;
  }
});
