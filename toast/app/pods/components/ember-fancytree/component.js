import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'table',
  classNames: ['table', 'table-condensed'],
  data: [],
  fancyTree: null,
  didInsertElement: function() {
    this.set('fancyTree', this.$().fancytree({
      checkbox: true,
      tabbable: false,
      extensions: ['table'],
      source: this.get('data'),
      renderColumns: function(event, data) {
        let node = data.node,
        $tdList = $(node.tr).find(">td");
        $tdList.eq(1).text(node.data.value);
        $tdList.eq(2).text(node.data.type);
      },
      table: {
        nodeColumnIdx: 0,
        checkboxColumnIdx: 1,
      },
    }));
  }
});
