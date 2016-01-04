import os
import json
import shutil
from jam.backends.base import Backend


class GitBackend(Backend):

    def __init__(self, location):
        self.location = location
        os.makedirs(location, exist_ok=True)

    def get(self, key):
        path = os.path.join(self.location, key[:2], key[2:])

        with open(path) as fileobj:
            return json.load(fileobj)

    def set(self, key, value):
        prefix, postfix = key[:2], key[2:]

        path = os.path.join(self.location, prefix)
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, postfix)

        with open(path, 'w') as fileobj:
            fileobj.write(json.dumps(value))

    def unset(self, key):
        os.remove(os.path.join(self.location, key[:2], key[2:]))

    def keys(self):
        files = list(os.scandir(self.location))
        while files:
            cur = files.pop(0)
            if cur.is_file():
                yield ''.join(cur.path.split('/')[-2:])
            else:
                files.extend(list(os.scandir(cur.path)))

    def unset_all(self):
        shutil.rmtree(self.location)
