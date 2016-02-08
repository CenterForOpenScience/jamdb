import JamAdapter from 'toast/mixins/jam-adapter';

export default JamAdapter.extend({
    queryUrlTemplate: '{+host}/v1/id/collections{/collectionId}/_search',

    urlSegments: {
        collectionId(type, id, snapshot, query) {
          let collectionId = query.collection.id;
          delete query.collection;
          return collectionId;
        }
    }
});
