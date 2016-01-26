import Ember from 'ember';


export default Ember.Mixin.create({
  attrs: {
    createdOn: {serialize: false},
    createdBy: {serialize: false},
    modifiedOn: {serialize: false},
    modifiedBy: {serialize: false},
  },

  normalize(model, payload) {
    payload.attributes = Object.assign({}, payload.attributes, payload.meta);
    return this._super(...arguments);
  }
});
