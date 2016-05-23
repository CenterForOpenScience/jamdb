import pytest

from collections import OrderedDict

from jam.models import DataObject


class TestReadOnlyStorage:

    def test_has_no_create(self, readonlystorage):
        with pytest.raises(AttributeError):
            readonlystorage.create({'test': 'data'})

    def test_repr(self, readonlystorage):
        assert isinstance(repr(readonlystorage), str)


class TestStorage:

    def test_create(self, storage):
        obj = storage.create({
            'test': 'data'
        })

        assert isinstance(obj, DataObject)
        assert obj.data == {'test': 'data'}

    def test_dedups(self, storage):
        objects = [
            storage.create({'test': 'data'})
            for _ in range(10)
        ]

        assert len(list(storage._backend.list())) == 1
        assert len({obj.ref for obj in objects}) == 1

    def test_orders_and_dedups(self, storage):
        objects = [
            storage.create(data)
            for data in (
                OrderedDict([('a', 1), ('b', 2), ('c', 3)]),
                OrderedDict([('b', 2), ('a', 1), ('c', 3)]),
                OrderedDict([('c', 3), ('b', 2), ('a', 1)]),
                OrderedDict([('a', 1), ('c', 3), ('b', 2)]),
            )
        ]

        assert len(list(storage._backend.list())) == 1
        assert len({obj.ref for obj in objects}) == 1

    def test_get(self, storage):
        data = (
            {'foo': 'bar'},
            {'bar': 'foo'},
            {'bar': 'baz'},
        )

        objects = [storage.create(datum) for datum in data]

        for dataobject, datum in zip(objects, data):
            assert storage.get(dataobject.ref).data == datum

    def test_bulk_read(self, storage):
        data = (
            {'foo': 'bar'},
            {'bar': 'foo'},
            {'bar': 'baz'},
        )

        objects = [storage.create(datum) for datum in data]
        read = [obj.data for obj in storage.bulk_read([dataobject.ref for dataobject in objects])]

        assert len(read) == len(objects)
        for datum in read:
            assert datum in data

    def test_repr(self, storage):
        assert isinstance(repr(storage), str)
