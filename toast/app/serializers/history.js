import DS from 'ember-data';

export default DS.JSONAPISerializer.extend({
  normalize(model, payload) {
    payload.attributes = Object.assign({}, payload.meta, payload.attributes);
    return this._super(model, payload);
  }
});
