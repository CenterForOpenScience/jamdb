from iodm.util import generate_id

import datetime
import weakref
import inspect


class CreateCollectionAction():
    def __init__(self, collection, log):
        pass

    def redo(self):
        pass

    def undo(self):
        pass

    def validate(self):
        pass


class RenameCollectionAction():
    def __init__(self, collection, log):
        self.collection = collection
        self.log = log

    def redo(self):
        pass

    def undo(self):
        pass

    def validate(self):
        self.log.exists(self.collection.name)


class Collection():

    operations = {}

    def __new__(cls, *args, **kwargs):
        for key, value in cls.__dict__.items():
            if inspect.isfunction(value) and hasattr(value, '__is_action__'):
                print(key)
        instance = super().__new__(cls)
        return instance

    def __init__(self, uid=None, name=None, storage=None, log=None, snapshot=None):
        self.name = name

        self._storage = storage
        self._log = log
        self._snapshot = snapshot

        if not uid:
            self.uid = generate_id()

            self.log('create_collection', {
                'name': self.name
            })

    def operation(fn):
        def wrapped(self, *args, **kwargs):
            return fn(self, *args, **kwargs)
        wrapped.__is_action__ = True
        wrapped.__name__ = fn.__name__
        return wrapped

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = uid

    @property
    def name(self):
        return self._collection_name

    @name.setter
    def name(self, name):
        self._collection_name = name

    def log(self, action, params):
        self._log.write(self.uid, action, params)

    def get_data(self, key):
        hash_string = self._snapshot.get_hash(key)
        return self._storage.read(hash_string)

    @operation
    def add(self, key, data):

        hash_string = self._storage.write(data)

        self.log('create', {
            'key': key,
            'data': hash_string
        })

        self._snapshot.add(key, hash_string)

    @operation
    def update(self, key, data):

        hash_string = self._storage.write(data)

        self.log('update', {
            'key': key,
            'data': hash_string
        })

        self._snapshot.update(key, hash_string)

    @operation
    def rename(self, original_key, new_key):
        self.log('rename', {
            'from': original_key,
            'to': new_key
        })
        self._snapshot.rename(original_key, new_key)

    @operation
    def remove(self, key):
        self.log('delete', {})
        self._snapshot.remove(key)

    @operation
    def rename_collection(self, new_name):
        self.log('rename_collection', {
            'from': self.name,
            'to': new_name
        }) # todo handle a break here on processing
        self._log.rename(self._collection_name, new_name)
        self.name = new_name
