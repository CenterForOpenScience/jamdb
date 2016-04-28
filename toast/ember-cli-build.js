/*jshint node:true*/
/* global require, module */
var EmberApp = require('ember-cli/lib/broccoli/ember-app');

module.exports = function(defaults) {
  var app = new EmberApp(defaults, {
      storeConfigInMeta: false,
    // Add options here
  });


  app.import('bower_components/lodash/lodash.js');
  app.import('bower_components/moment/moment.js');

  app.import('bower_components/jsoneditor/dist/jsoneditor.css');
  app.import('bower_components/jsoneditor/dist/jsoneditor.js');
  app.import('bower_components/jsoneditor/dist/img/jsoneditor-icons.svg', {destDir: 'assets/img'});

  app.import('bower_components/jquery-ui/jquery-ui.js');
  app.import('bower_components/jquery.fancytree/dist/jquery.fancytree-all.js');
  app.import('bower_components/jquery.fancytree/dist/skin-awesome/ui.fancytree.css');


  app.import('bower_components/bootstrap/dist/js/bootstrap.js');
  app.import('bower_components/bootstrap/dist/css/bootstrap.css');

  app.import('bower_components/AdminLTE/dist/css/AdminLTE.css');
  // app.import('bower_components/AdminLTE/dist/css/skins/skin-black-light.css');
  app.import('bower_components/AdminLTE/dist/css/skins/_all-skins.css');

  app.import('bower_components/font-awesome/css/font-awesome.css');
  app.import('bower_components/font-awesome/fonts/fontawesome-webfont.eot', {destDir: 'fonts'});
  app.import('bower_components/font-awesome/fonts/fontawesome-webfont.svg', {destDir: 'fonts'});
  app.import('bower_components/font-awesome/fonts/fontawesome-webfont.ttf', {destDir: 'fonts'});
  app.import('bower_components/font-awesome/fonts/fontawesome-webfont.woff', {destDir: 'fonts'});
  app.import('bower_components/font-awesome/fonts/fontawesome-webfont.woff2', {destDir: 'fonts'});
  app.import('bower_components/font-awesome/fonts/FontAwesome.otf', {destDir: 'fonts'});

  // app.import('bower_components/x-editable/dist/bootstrap3-editable/js/bootstrap-editable.js');
  // app.import('bower_components/x-editable/dist/bootstrap3-editable/css/bootstrap-editable.css');

  // Use `app.import` to add additional libraries to the generated
  // output files.
  //
  // If you need to use different assets in different
  // environments, specify an object as the first parameter. That
  // object's keys should be the environment name and the values
  // should be the asset to use in that environment.
  //
  // If the library that you are including contains AMD or ES6
  // modules that you would like to import into your application
  // please specify an object with the list of modules as keys
  // along with the exports of each module as its value.

  return app.toTree();
};
