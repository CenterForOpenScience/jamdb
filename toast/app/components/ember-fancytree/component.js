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
  classNames: ['table', 'table-condensed'],
  didInsertElement: function() {
    let self = this;

    this.set('fancyTree', this.$().fancytree({
      tabbable: false,
      extensions: ['table', 'glyph'],
      glyph: GLYPH_OPTIONS,
      table: TABLE_OPTIONS,
      source: this.get('data'),
      click: (event, data) => {

      },
      renderColumns: function(event, data) {
        let node = data.node,
        $tdList = $(node.tr).find('>td');
        $tdList.eq(1).text(node.data.value);
        $tdList.eq(2).append(node.data.type + ' ');
        if (node.parent.parent == null) {
          $tdList.eq(2).append($('<i class="fa fa-gear"></i>'));
          $tdList.eq(2).append($('<i class="fa fa-history"></i>').click(function() {
            self.sendAction('history', node.title);
          }));
        }
      },
    }));
  }
});
