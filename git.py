import os
import json

import jtake


class StorageEngine:

    def __init__(self, dir_loc):
        self.dir_loc = dir_loc

    def write(self, key, data):
        try:
            os.makedirs(os.path.join(self.dir_loc, key[:2]))
        except FileExistsError:
            pass
        path = os.path.join(self.dir_loc, key[:2], key[2:])
        with open(path, 'w') as fileobj:
            fileobj.write(json.dumps(data))

    def __iter__(self):
        files = list(os.scandir(self.dir_loc))
        while files:
            cur = files.pop(0)
            if cur.is_file():
                yield ''.join(cur.path.split('/')[-2:])
            else:
                files.extend(list(os.scandir(cur.path)))

    def read(self, key):
        path = os.path.join(self.dir_loc, key[:2], key[2:])
        try:
            with open(path) as fileobj:
                return json.load(fileobj)
        except FileNotFoundError:
            return None


class JSONDataObject(jtake.JSONDataObject):
    file_loc = 'data/blobs'
    StorageEngineClass = StorageEngine


class Snapshot(jtake.take.Snapshot):
    DataObjectClass = JSONDataObject


class OpLog(jtake.take.OpLog):
    file_loc = 'data/logs'
    StorageEngineClass = StorageEngine


class Collection(jtake.Collection):
    SnapshotClass = Snapshot
    OperationLogClass = OpLog
    DataObjectClass = JSONDataObject
