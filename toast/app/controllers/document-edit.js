import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    save(data) {
      console.log(data)
      this.set('model.attributes', data);
      this.get('model').save().then(() => Ember.$('.document-save').addClass('blink'));
    }
  }
});
