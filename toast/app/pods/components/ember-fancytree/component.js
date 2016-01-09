import Ember from 'ember';

const GLYPH_OPTIONS = {
  map: {
    checkbox: 'fa fa-square-o',
    checkboxSelected: 'fa fa-check-square-o',
    checkboxUnknown: 'fa fa-square',
    dragHelper: 'fa arrow-right',
    dropMarker: 'fa long-arrow-right',
    error: 'fa fa-warning',
    expanderClosed: 'fa fa-caret-right',
    expanderLazy: 'fa fa-angle-right',
    expanderOpen: 'fa fa-caret-down',
    doc: 'fa fa-file-o',
    docOpen: 'fa fa-file-o',
    folder: 'fa fa-folder-o',
    folderOpen: 'fa fa-folder-open-o',
    loading: 'fa fa-spinner fa-pulse'
  }
};

const TABLE_OPTIONS = {
  nodeColumnIdx: 0,
  // checkboxColumnIdx: 1,
};

export default Ember.Component.extend({
  data: [],
  fancyTree: null,
  tabbable: false,
  tagName: 'table',
  titlesTabbable: false,
  classNames: ['table', 'table-condensed', 'table-striped'],
  didInsertElement: function() {
    // Ember.$.fn.editable.defaults.mode = 'inline';

    // Ember.$.fn.editableform.buttons = '<button type="submit" class="btn btn-primary btn-sm editable-submit"><i class="fa fa-check"></i></button><button type="button" class="btn btn-default btn-sm editable-cancel"><i class="fa fa-remove"></i></button>';


    this.set('fancyTree', this.$().fancytree({
      tabbable: false,
      extensions: ['table', 'glyph'],
      glyph: GLYPH_OPTIONS,
      table: TABLE_OPTIONS,
      source: this.get('data'),
      renderColumns: function(event, data) {
        let node = data.node,
        $tdList = $(node.tr).find('>td');
        $tdList.eq(1).text(node.data.value);
        // if (node.data.editable) {
        //   $tdList.eq(1).append($('<a></a>').text(node.data.value).addClass('editable'));
        // } else {
        //   $tdList.eq(1).text(node.data.value);
        // }
        $tdList.eq(2).text(node.data.type);
      },
    }));
    // this.$().editable({
    //   type: 'text',
    //   selector: '.editable',
    //   tpl: '<input type="text">',
    // });
  }
});
