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
            text: attr,
            data: {
                attr: obj[attr]
            }
        };
    });
}

export default Ember.Controller.extend({
    adapterContext: Ember.inject.service(),

    selectedID: null,
    page: 1,
    queryParams: ['page'],
    jsTreeOptions: {
        columns: [
            {header: "Nodes", width: '100%'},
            // {width: 30, header: "Price", value: "price"}
        ]
    },

    documents: function() {
        return this.get('model.namespace').then(namespace => {
            this.set('adapterContext.namespace', namespace);
            this.set('adapterContext.collection', this.get('model'));
            return this.store.query('document', {
                page: this.get('page'),
            });
        });
    }.property('model', 'page'),
    jsTreeData: function() {
        let self = this;
        return Ember.ObjectProxy.extend(Ember.PromiseProxyMixin).create({
            promise: new Ember.RSVP.Promise(resolve =>
                self.get('documents').then(docs => resolve({data: docs.map(el => ({
                        id: el.get('id'),
                        icon: 'fa fa-map',
                        text: el.get('id'),
                        children: objectToJsTree(el.get('data.attributes'))
            }))})))
        });
    }.property('documents'),

    actions: {
        jsTreeChange(event) {
            if (event.selected.length != 1) return;
            if (this.get('selectedID') == event.selected[0]){
                return this.transitionToRoute('namespace.collection.document', event.selected[0]);
            }
            this.set('selectedID', event.selected[0]);
        },
        nextPage(event) {
            this.transitionToRoute({ queryParams: { page: this.get('page') + 1 }});
        }
    }
});
