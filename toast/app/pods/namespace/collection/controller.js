import Ember from 'ember';


function objectToJsTree(obj) {
    return Object.keys(obj).map((attr) => {
        if (Array.isArray(obj[attr]))
            return {
                text: attr,
                icon: 'fa fa-list',
                children: obj[attr].map((val, i) => ({text: i, children: [objectToJsTree(val)]}))
            };
        if (typeof(obj[attr]) === typeof({}))
            return {
                text: attr,
                icon: 'fa fa-map',
                children: objectToJsTree(obj[attr])
            };
        return {
            icon: 'fa fa-quote-right',
            text: `${attr}: ${obj[attr]}`
        };
    });
}

export default Ember.Controller.extend({
    attributes: [],
    isLoading: true,
    pluging: ['wholerow'],
    jsTreeData: function() {
        return this.get('model.documents').map(el => ({
            icon: 'fa fa-map',
            text: el.get('id'),
            children: objectToJsTree(el.get('data.attributes'))
        }));
    }.property('model')
});
