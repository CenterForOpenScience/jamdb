import Base from 'ember-simple-auth/authenticators/base';

const { RSVP } = Ember;

export default Base.extend({
    url: 'http://localhost:1212/v1/auth',
    restore(data) {
        //TODO when to reject? Maybe restore here?
        return new RSVP.Promise((resolve, reject) => {
            resolve(data);
        });
    },
    authenticate(namespace, username, password) {
        var request = Ember.$.ajax({
            method: 'POST',
            url: this.url,
            dataType: 'json',
            contentType: 'application/json',
            xhrFields: {withCredentials: true},
            data: JSON.stringify({data: {
                type: 'users',
                attributes: {
                    provider: 'self',
                    collection: 'users',
                    namespace: namespace,
                    username: username,
                    password: password,
                }
            }})
        });

        return new RSVP.Promise((resolve, reject) => {
            request
            .then((data) => resolve(data.data))
            .fail(() => reject());
        });
    },
    invalidate(data) {

    }
});
