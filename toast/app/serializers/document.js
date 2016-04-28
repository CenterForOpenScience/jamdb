import DS from 'ember-data';

export default DS.JSONAPISerializer.extend({
  normalize(model, payload) {
    payload.attributes = Object.assign({}, payload.meta, {attributes: payload.attributes});
    return this._super(model, payload);
  },
  serialize(snapshot, options) {
    var data = this._super(snapshot, options);
    data.data.attributes = data.data.attributes.attributes;
    return data;
  }
});
