import Ember from 'ember';

let PermissionsEditor = Ember.Component.extend({
  tagName: 'table',
  classNames: ['table'],
  permissionLevels: [
    'CREATE',
    'READ',
    'UPDATE',
    'DELETE',
    'ADMIN',
  ],

  newPermissionLevel: 'CREATE',
  newPermissionSelector: '',

  actions: {
    addPermission() {
      this.permissions[this.get('newPermissionSelector')] = this.get('newPermissionLevel');
      this.set('newPermissionSelector', '');
      this.get('onchange')(this.get('permissions'));
      this.rerender();
    },
    removePermission(key) {
      delete this.permissions[key];
      this.get('onchange')(this.get('permissions'));
      this.rerender();
    }
  }
});

PermissionsEditor.reopenClass({
  positionalParams: ['permissions'],
});


export default PermissionsEditor;
