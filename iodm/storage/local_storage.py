from iodm.storage.base import Storage
from iodm.util import get_checksum

import hashlib
import io
import os


class LocalStorage(Storage):

    def __init__(self, *args, **kwargs):
        self._path = kwargs.get('path', None)
        self._hash_cls = kwargs.get('hash', hashlib.sha1)

    def _make_data_object_path(self, hash_string):
        return os.path.join(self._make_data_object_directory_path(hash_string), hash_string[2:])

    def _make_data_object_directory_path(self, hash_string):
        return os.path.join(self._path, hash_string[0:2])

    def _write_data(self, fp):
        data_id = get_checksum(fp, algo=self._hash_cls)

        if not os.path.exists(self._make_data_object_path(data_id)):
            try:
                os.makedirs(self._make_data_object_directory_path(data_id))
            except:
                pass
            with open(self._make_data_object_path(data_id), 'w') as writer:
                fp.seek(0)
                writer.write(fp.read())
        return data_id

    def write(self, value, **kwargs):
        fp = io.StringIO(value)
        hash_string = self._write_data(fp)
        fp.close()
        return hash_string

    def read(self, hash_string, validate=False, **kwargs):
        with open(self._make_data_object_path(hash_string), 'r') as fp:
            data = fp.read()
        if validate:
            sha = hashlib.sha1()
            sha.update(data.encode('utf-8'))
            assert key == sha.hexdigest()
        return data