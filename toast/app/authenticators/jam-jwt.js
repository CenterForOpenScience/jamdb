import Ember from 'ember';
import Base from 'ember-simple-auth/authenticators/base';

const { $, RSVP } = Ember;

export default Base.extend({
    url: 'http://localhost:1212/v1/auth',
    restore(data) {
        let token = JSON.parse(atob(data.attributes.token.split('.')[1]));
        if (token.exp > moment().unix())
          return RSVP.resolve(data);
        return RSVP.reject(data);
    },
    authenticate(attrs) {
        return $.ajax({
            method: 'POST',
            url: this.url,
            dataType: 'json',
            contentType: 'application/json',
            xhrFields: {withCredentials: true},
            data: JSON.stringify({data: {
                type: 'users',
                attributes: attrs
            }})
        }).then(data => data.data);
    }
    // invalidate(data) {
    //     debugger;
    // }
});
