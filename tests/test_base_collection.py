import pytest

from jam import exceptions
from jam.base import BaseCollection
from jam.base import Operation
import jam


@pytest.fixture
def collection(storage, logger, state):
    return BaseCollection(storage, logger, state)


@pytest.mark.skip(reason='Unimplemented Test')
class TestReadOnlyCollection:

    def test_from_document(self):
        pass

    def test_from_dict(self):
        pass

    def test_load_schema(self):
        pass

    def test_regenerate(self):
        pass

    def test_load_snapshot(self):
        pass


class TestCollectionDateInteraction:
    user = 'tester'

    def test_create_read(self, sampledata, collection):
        for doc in sampledata:
            collection.create(doc.ref, doc.data, self.user)

        for doc in sampledata:
            assert collection.read(doc.ref).data == doc.data

    def test_create_dups(self, sampledata, collection):
        for doc in sampledata:
            collection.create(doc.ref, doc.data, self.user)

        for doc in sampledata:
            with pytest.raises(exceptions.KeyExists) as e:
                collection.create(doc.ref, doc.data, self.user)
            assert doc.ref in e.value.detail

    def test_update_must_exist(self, sampledata, collection):
        for doc in sampledata:
            with pytest.raises(exceptions.NotFound):
                collection.update(doc.ref, doc.data, self.user)

    def test_update(self, sampledata, collection):
        for doc in sampledata:
            collection.create(doc.ref, doc.data, self.user)
            collection.update(doc.ref, {v: k for k, v in doc.data.items()}, self.user)

        for doc in sampledata:
            assert collection.read(doc.ref).data == {v: k for k, v in doc.data.items()}

    def test_delete(self, sampledata, collection):
        for doc in sampledata:
            collection.create(doc.ref, doc.data, self.user)

        for doc in sampledata:
            collection.read(doc.ref)

        for doc in sampledata:
            collection.delete(doc.ref, self.user)

        for doc in sampledata:
            with pytest.raises(exceptions.NotFound):
                collection.read(doc.ref)

    def test_keys(self, sampledata, collection):
        for i in range(len(sampledata)):
            doc = sampledata[i]
            collection.create(doc.ref, doc.data, self.user)
            assert sorted(collection.keys()) == sorted(x.ref for x in sampledata[:i + 1])

    def test_list(self, sampledata, collection):
        for i in range(len(sampledata)):
            doc = sampledata[i]
            collection.create(doc.ref, doc.data, self.user)
            assert [
                x.data for x in
                sorted((x for x in collection.list()), key=lambda x: x.ref)
            ] == [
                x.data for x in
                sorted((x for x in sampledata[:i + 1]), key=lambda x: x.ref)
            ]

    def test_rename(self, sampledata, collection):
        for doc in sampledata:
            collection.create(doc.ref, doc.data, self.user)

        for doc in sampledata:
            collection.read(doc.ref)

        for doc in sampledata:
            collection.rename(doc.ref, doc.ref[::-1], self.user)

        for doc in sampledata:
            collection.read(doc.ref[::-1])
            with pytest.raises(exceptions.NotFound):
                collection.read(doc.ref)

    def test_regenerate(self, sampledata, collection):
        for doc in sampledata:
            collection.create(doc.ref, doc.data, self.user)

        collection._state.clear()

        for doc in sampledata:
            with pytest.raises(exceptions.NotFound):
                collection.read(doc.ref)

        collection.regenerate()

        assert [
            x.data for x in
            sorted((x for x in collection.list()), key=lambda x: x.ref)
        ] == [
            x.data for x in
            sorted((x for x in sampledata), key=lambda x: x.ref)
        ]

    def test_regenerate_complex(self, sampledata, collection):
        for doc in sampledata:
            collection.create(doc.ref, doc.data, self.user)
            collection.delete(doc.ref, self.user)
            collection.create(doc.ref, doc.data, self.user)
            collection.update(doc.ref, doc.data, self.user)

        collection._state.clear()

        for doc in sampledata:
            with pytest.raises(exceptions.NotFound):
                collection.read(doc.ref)

        collection.regenerate()

        assert [
            x.data for x in
            sorted((x for x in collection.list()), key=lambda x: x.ref)
        ] == [
            x.data for x in
            sorted((x for x in sampledata), key=lambda x: x.ref)
        ]

    def test_history(self, sampledata, collection):
        for doc in sampledata:
            collection.create(doc.ref, doc.data, self.user)
            collection.delete(doc.ref, self.user)
            collection.create(doc.ref, doc.data, self.user)
            collection.update(doc.ref, doc.data, self.user)

        for doc in sampledata:
            assert [x.operation for x in collection.history(doc.ref)] == [Operation.UPDATE, Operation.CREATE, Operation.DELETE, Operation.CREATE]

    def test_replace(self, sampledata, collection):
        pass

    def test_update_jsonpatch(self, sampledata, collection):
        pass

    def test_update_schema_validation(self, sampledata, collection):
        pass

    def test_update_jsonpatch_test(self, sampledata, collection):
        pass

    def test_snapshot(self, sampledata, collection):
        for doc in sampledata:
            collection.create(doc.ref, doc.data, self.user)
            collection.delete(doc.ref, self.user)
            collection.create(doc.ref, doc.data, self.user)
            collection.update(doc.ref, doc.data, self.user)

        log = collection.snapshot()
        blobs = [x.data for x in sampledata]
        for k, v in collection._storage.get(log.data_ref).data:
            blobs.remove(collection._storage.get(v).data)
        assert len(blobs) == 0

        collection._state.clear()

        for doc in sampledata:
            with pytest.raises(exceptions.NotFound):
                collection.read(doc.ref)

        assert collection.regenerate() == 0

        assert [
            x.data for x in
            sorted((x for x in collection.list()), key=lambda x: x.ref)
        ] == [
            x.data for x in
            sorted((x for x in sampledata), key=lambda x: x.ref)
        ]


@pytest.mark.skip(reason='Unimplemented Test')
class TestBaseCollection:
    pass
