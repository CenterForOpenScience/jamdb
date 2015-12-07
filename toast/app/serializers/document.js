import DS from 'ember-data';


//TODO override serialize as well
export default DS.JSONAPISerializer.extend({
  normalize(model, payload) {
      payload.attributes = Object.assign({}, payload.meta, {attributes: payload.attributes});
      delete payload.meta;
    return this._super(model, payload);
  }
});
