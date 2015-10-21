from iodm.storage.local_storage import LocalStorage
from iodm.collection import Collection
from iodm.log import Log
from iodm.tree import Tree

import os

if __name__ == '__main__':
    storage = LocalStorage(path='db/data_objects') # todo Variability?

    log = Log(path='db/logs')
    tree = Tree()

    collection = Collection(name='notes', storage=storage, log=log, tree=tree)
    print(collection.uid)
    print(Collection.actions)
    collection.add(key='first', data="hello, world")
    collection.rename_collection('notebook')
    collection.rename('first', 'second')
    print(collection.get_data('second'))