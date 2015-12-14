/* jshint node: true */
'use strict';


var path = require('path');


module.exports = {
  name: 'ember-admin-lte',
  blueprintsPath: () => path.join(__dirname, 'blueprints'),
  included: function(app) {
      this._super.included(this);
      this.app.import(app.bowerDirectory + '/bootstrap/dist/css/bootstrap.css');
      // this.app.import(app.bowerDirectory + '/bootstrap/dist/fonts/glyphicons-halflings-regular.eot', { destDir: 'fonts' });
      // this.app.import(app.bowerDirectory + '/bootstrap/dist/fonts/glyphicons-halflings-regular.svg', { destDir: 'fonts' });
      // this.app.import(app.bowerDirectory + '/bootstrap/dist/fonts/glyphicons-halflings-regular.ttf', { destDir: 'fonts' });
      // this.app.import(app.bowerDirectory + '/bootstrap/dist/fonts/glyphicons-halflings-regular.woff', { destDir: 'fonts' });
      // this.app.import(app.bowerDirectory + '/bootstrap/dist/fonts/glyphicons-halflings-regular.woff2', { destDir: 'fonts' });

      this.app.import(app.bowerDirectory + '/font-awesome/css/font-awesome.css');
      this.app.import(app.bowerDirectory + '/font-awesome/fonts/fontawesome-webfont.eot', { destDir: 'fonts' });
      this.app.import(app.bowerDirectory + '/font-awesome/fonts/fontawesome-webfont.svg', { destDir: 'fonts' });
      this.app.import(app.bowerDirectory + '/font-awesome/fonts/fontawesome-webfont.ttf', { destDir: 'fonts' });
      this.app.import(app.bowerDirectory + '/font-awesome/fonts/fontawesome-webfont.woff', { destDir: 'fonts' });
      this.app.import(app.bowerDirectory + '/font-awesome/fonts/fontawesome-webfont.woff2', { destDir: 'fonts' });
      this.app.import(app.bowerDirectory + '/font-awesome/fonts/FontAwesome.otf', { destDir: 'fonts' });

      this.app.import(app.bowerDirectory + '/admin-lte/dist/css/AdminLTE.css');
      this.app.import(app.bowerDirectory + '/admin-lte/dist/css/skins/_all-skins.css');
      // this.app.import(app.bowerDirectory + `/admin-lte/dist/css/skins/skin-${app.options['ember-admin-lte'].skin || 'blue'}.css`);
  },
  isDevelopingAddon: function() {
    return true;
  }
};
