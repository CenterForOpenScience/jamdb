var MM_URL = 'http://localhost:1212/';
var SHARE = 'SHARE';
var DOCUMENTS = 'share-data';
var CURATIONS = 'curations';

$(document).ready(function(){
    var documents = [];

    function loadAll(url, page, accu) {
        page = page || 1;
        accu = accu || [];
        return $.ajax({
            method: 'GET',
            url: url,
            dataType: 'json',
            contentType: 'application/json',
            xhrFields: {withCredentials: true},
        }).then(function(data) {
            accu = accu.concat(data.data);
            if (data.meta.total > accu.length) {
                return loadAll(url, page + 1, accu);
            }
            return accu;
        });
    }

    function loadDocuments() {
        loadAll(MM_URL + 'v1/namespaces/' + SHARE + '/collections/' + DOCUMENTS + '/documents/').then(function(docs) {
            documents = docs;
            $('#shareDocuments').html(documents.map(function(item){
                return '<div class="share-document alert alert-info" data-id="'+item.id+'"><a>' + item.attributes.title + '</a></div>';
            }));
        });
    }

    $('#shareDocuments').on('click', '.share-document', function() {
        var self = $(this);
        $('.selected').removeClass('selected');
        $(this).addClass('selected');
        $('#selectedDocument').val(JSON.stringify(documents.find(function(doc) {
            return doc.id === self.data('id').toString();
        }).attributes, null, '  '));
    });

    $('#save').on('click', function() {
        var selectedID = $('.selected').data('id');
        var curated = JSON.parse($('#selectedDocument').val());
        var original = documents.find(function(doc) {
            return doc.id === selectedID;
        });

        var diff = diffObjects(original.attributes, curated);
        $.ajax({
            method: 'POST',
            url: MM_URL + ['v1', 'namespaces', SHARE, 'collections', CURATIONS, 'documents'].join('/'),
            dataType: 'json',
            xhrFields: {withCredentials: true},
            contentType: 'application/json',
            data: JSON.stringify({
                data: {
                    type: 'document',
                    attributes: {document: selectedID, curation: diff}
                }
            })
        });
    });

    function diffObjects(obj1, obj2) {
        var diff = {};
        var keys = new Set(Object.keys(obj1).concat(Object.keys(obj2)));
        keys.forEach(function(key) {
            if (!!obj1[key] && !!obj2[key] && typeof(obj1[key]) === 'object' && typeof(obj2[key]) === 'object') {
                var tmp = diffObjects(obj1[key], obj2[key]);
                if (Object.keys(tmp).length > 0)
                    diff[key] = tmp;
            } else if (obj1[key] !== obj2[key]) {
                diff[key] = {
                    updated: obj2[key],
                    original: obj1[key],
                };
            }
        });
        return diff;
    }

    function login() {
        $.ajax({
            method: 'POST',
            url: MM_URL + 'v1/auth',
            dataType: 'json',
            contentType: 'application/json',
            xhrFields: {withCredentials: true},
            data: JSON.stringify({data: {
                type: 'users',
                attributes: {
                    provider: 'self',
                    namespace: 'SHARE',
                    collection: 'users',
                    username: 'chris',
                    password: 'password'
                }
            }})
        }).done(function(data) {
            document.cookie = 'cookie=' + data.data.attributes.token;
        });
    }

    (function() {
        login();
        loadDocuments();
    })();
});
