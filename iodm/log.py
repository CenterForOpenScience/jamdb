from iodm import VERSION

import datetime
import json
import os
import shutil
import pathlib


class Log():
    def __init__(self, *args, **kwargs):
        self._path = kwargs.get('path', None)

    def rotate(self):
        pass

    def exists(self, uid):
        return os.path.exists(os.path.join(self._path, uid, 'current.log'))

    def rename(self, collection, new_name):
        # try:
        #     shutil.copytree(os.path.join(self._path, collection), os.path.join(self._path, new_name))
        # except FileExistsError:
        #     raise Exception('Collection names must be unique')
        # for dirpath, dirnames, filenames in os.walk(os.path.join(self._path, collection)):
        #     for filename in filenames:
        #         os.remove(os.path.join(dirpath, filename))
        # os.removedirs(os.path.join(self._path, collection))
        pass

    def write(self, uid, action, params):
        log_path = os.path.join(self._path, uid)

        try:
            os.makedirs(log_path)
        except:
            pass

        with open(os.path.join(log_path, 'current.log'), 'a') as f:
            f.write(json.dumps({
                'version': VERSION,
                'collection': uid,
                'action': action,
                'datetime': str(datetime.datetime.utcnow()),
                'params': params
            }) + os.linesep)
