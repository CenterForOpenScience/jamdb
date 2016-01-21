/* jshint node: true */

module.exports = function(environment) {
  var ENV = {
    jamdbURL: 'http://localhost:1212',
    OSF: {
        clientId: 'db1ff76b6001460c884c33b74b2784f8',
        scope: 'osf.users.all_read',
        url: 'https://staging-accounts.osf.io',
    },
    modulePrefix: 'toast',
    environment: environment,
    baseURL: '/',
    locationType: 'auto',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      }
    },
    'ember-simple-auth': {
        authenticationRoute: 'login'
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    },
    contentSecurityPolicy: {
        'font-src': "'self' fonts.gstatic.com fonts.googleapis.com",
        'style-src': "'self' 'unsafe-inline' fonts.googleapis.com",
        'connect-src': "'self' localhost:1212",
        'child-src': "'self' blob:",
    }
  };

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.baseURL = '/';
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
  }

  if (environment === 'production') {

  }

  return ENV;
};
