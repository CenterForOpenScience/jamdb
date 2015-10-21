from iodm.storage.local_storage import LocalStorage

import os
import tempfile
import unittest

class TestStringMethods(unittest.TestCase):

    def test_write(self):
        dir = tempfile.gettempdir()
        storage = LocalStorage(path=dir)

        key = storage.write('test')

        file_path = storage._make_data_object_path(key)
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, 'r') as f:
            self.assertEquals(f.read(), 'test')

    def test_write_and_read(self):
        dir = tempfile.gettempdir()
        storage = LocalStorage(path=dir)

        key = storage.write('test2')
        file_path = storage._make_data_object_path(key)
        self.assertEquals(storage.read(key), 'test2')

if __name__ == '__main__':
    unittest.main()