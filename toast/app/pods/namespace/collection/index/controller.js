import Ember from 'ember';

const TYPE_MAP = {
  'string': 'fa fa-quote-right'
};


function objectToJsTree(obj) {
    return Object.keys(obj).map((attr) => {
        if (Array.isArray(obj[attr]))
          return {
            title: attr,
            icon: 'fa fa-list',
            data: {
              value: `Array [${obj[attr].length}]`,
              type: 'Array',
            },
            children: obj[attr].map((val, i) => objectToJsTree({[i]: val})[0])
          };
        if (typeof(obj[attr]) === typeof({}))
            return {
                title: attr,
                data: {
                  value: `{ ${Object.keys(obj[attr]).length} fields }`,
                    type: 'Object'
                },
                children: objectToJsTree(obj[attr])
            };
        return {
          icon: TYPE_MAP[typeof obj[attr]],
          title: attr,
          data: {
            editable: true,
            value: obj[attr],
            type: (typeof obj[attr]).capitalize()
          }
        };
    });
}

export default Ember.Controller.extend({
    adapterContext: Ember.inject.service(),

    selectedID: null,
    page: 1,
    totalPages: 0,
    queryParams: ['page'],
    hasPrev: function() {
      return this.get('page') > 1;
    }.property('page', 'totalPages'),
    hasNext: function() {
      return this.get('page') < this.get('totalPages');
    }.property('page', 'totalPages'),
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
            }).then(docs => {
              console.log(docs.get('meta'));
              this.set('totalPages', docs.get('meta.total') / docs.get('meta.perPage'));
              return docs;
            });
        });
    }.property('model', 'page'),
    jsTreeData: function() {
        let self = this;
        return Ember.ObjectProxy.extend(Ember.PromiseProxyMixin).create({
            promise: new Ember.RSVP.Promise(resolve =>
                self.get('documents').then(docs => resolve({data: docs.map(el => objectToJsTree({
                  [el.get('id')]: el.get('data.attributes')
                })[0])})))
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
        },
        prevPage(event) {
            this.transitionToRoute({ queryParams: { page: this.get('page') - 1 }});
        }
    }
});
