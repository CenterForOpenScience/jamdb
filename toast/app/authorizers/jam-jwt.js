import Base from 'ember-simple-auth/authorizers/base';

export default Base.extend({
  authorize(sessionData, block) {
      block('Authorization', sessionData.attributes.token);
  }
});
