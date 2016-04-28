import Ember from 'ember';
import EmberFancyTree from '../ember-fancytree/component';


export default EmberFancyTree.extend({
  renderColumns(event, data) {
    let node = data.node,
    $tdList = $(node.tr).find('>td');
    $tdList.eq(1).text(node.data.value);
    $tdList.eq(2).append(node.data.type + ' ');
  }
});
