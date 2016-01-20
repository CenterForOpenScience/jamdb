import Ember from 'ember';

const OPromise = Ember.ObjectProxy.extend(Ember.PromiseProxyMixin);
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

function tablify(docs) {
  return docs.map(el =>
    objectToJsTree({
      [el.get('id')]: el.get('data.attributes')
  })[0]);
}

//Ghetto hack
let doSearch = function() {
  let params = {
    page: this.get('page'),
    collection: this.get('model'),
    'page[size]': this.get('pageSize'),
  };

  if (this.get('queryText').trim().length > 0)
    params.q = this.get('queryText');

  this.set('tableData.promise', this.store
      .query('document', params)
      .then(docs => {
        this.set('totalPages', docs.get('meta.total') / docs.get('meta.perPage'));
        return docs;
      })
      .then(tablify));
};


export default Ember.Controller.extend({
    page: 1,
    pageSize: 50,
    totalPages: 0,
    queryText: '',
    queryParams: ['page', {'queryText': 'q'}],

    tableData: OPromise.create(),

    _init: function() {
      this.setProperties({
        'page': 1,
        'totalPages': 0,
        'queryText': ''
      });
      //Stop the triggered event
      //Better than hacking into ember...
      this.doSearch.cancel();
      this._doSearch();
    }.observes('model'),

    hasPrev: function() {
      return this.get('page') > 1;
    }.property('page', 'totalPages'),

    hasNext: function() {
      return this.get('page') < this.get('totalPages');
    }.property('page', 'totalPages'),

    search: function() {
      this.set('tableData', OPromise.create());
    }.observes('page', 'queryText'),

    _doSearch: doSearch,  //Allow for instant queries
    doSearch: _.debounce(doSearch, 500).observes('page', 'queryText'),

    actions: {
        historyClick(documentId) {
          this.transitionToRoute('document', documentId);
          return false;
        },
        nextPage(event) {
          this.incrementProperty('page');
        },
        prevPage(event) {
          this.decrementProperty('page');
        }
    }
});
