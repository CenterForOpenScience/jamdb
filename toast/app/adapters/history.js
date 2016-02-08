import JamAdapter from 'toast/mixins/jam-adapter';

export default JamAdapter.extend({
    queryUrlTemplate: '{+host}/v1/id/documents{/documentId}/history',

    urlSegments: {
        documentId(type, id, snapshot, query) {
          let dId = query.document.id;
          delete query.document;
          return dId;
        }
    }
});
