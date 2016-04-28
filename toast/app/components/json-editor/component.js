import Ember from 'ember';
// import JSONEditor from 'jsoneditor';
//

const {$} = Ember;
const DEFAULT_SCHEMA = {type: 'object'};

export default Ember.Component.extend({
  classNames: ['full-height'],

  json: {},
  name: '',
  editor: null,
  saveButton: null,

  options: function() {
    return {
      name: this.get('name'),
      schema: this.get('schema'),
      onChange: this.send.bind(this, 'change'),
    };
  }.property('name', 'schema'),

  didInsertElement() {
    this._super(...arguments);
    this.set('schema', this.get('schema') || DEFAULT_SCHEMA);
    this.set('editor', new JSONEditor(this.$()[0], this.get('options'), this.get('json')));
    this.set('saveButton', $('<button></button>')
      .on('click', this.send.bind(this, 'save'))
      .attr('disabled', true)
      .attr('title', 'Save')
      .addClass('document-save')
      .append($('<i></i>')
          .addClass('fa fa-floppy-o'))
      .insertBefore(this.$('.jsoneditor>.jsoneditor-menu>.jsoneditor-search')));
  },

  actions: {
    save() {
      this.get('saveButton').attr('disabled', true);//.addClass('blink');
      this.sendAction('save', this.get('editor').get());
    },
    change() {
      this.get('saveButton').attr('disabled', false).removeClass('blink');
      this.sendAction('change');
    }
  }
});
