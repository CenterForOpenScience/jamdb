from iodm import O
from iodm import Q
from iodm.base import Operation


class Collection:

    def __init__(self, storage, logger, snapshot, regenerate=True):
        self._logger = logger
        self._storage = storage
        self._snapshot = snapshot
        if regenerate:
            # Oddity with regenerate + snapshot
            self.regenerate()

    def regenerate(self):
        self._snapshot.clear()

        snapshot_log = self._logger.latest_snapshot()
        if snapshot_log:
            self.load_snapshot(snapshot_log)
            logs = self._logger.after(snapshot_log.timestamp)
        else:
            logs = self._logger.list(O('timestamp', 1))  # Ascending

        for log in logs:
            self._snapshot.apply(log)

        return True

    def load_snapshot(self, snapshot_log):
        data_object = self._storage.create(snapshot_log.data_ref)
        for log_ref in data_object.data:
            self._snapshot.apply(self._logger.get(log_ref), safe=False)

    def list(self):
        return self._snapshot.list()

    def create(self, key, data):
        data_object = self._storage.create(data)
        log = self._logger.create(Operation.CREATE, key, data_object.ref)
        return self._snapshot.apply(log, data_object)

    def read(self, key):
        return self._storage.get(self._snapshot.get(key).data_ref)

    def update(self, key, data, merger=None):
        if merger:
            original = self._snapshot.get(key)
            data = merger(original, data)
        data_object = self._storage.create(data)
        log = self._logger.create(Operation.UPDATE, key, data_object.ref)
        return self._snapshot.apply(log, data_object)

    def delete(self, key):
        # TODO ref or not?
        log = self._logger.create(Operation.DELETE, key, None)
        return self._snapshot.apply(log, None)

    def rename(self, key, new_key):
        original = self._snapshot.get(key)
        log = self._logger.create(Operation.RENAME, key, None, **{'to': new_key})
        self._snapshot.apply(log, None)

        log = self._logger.create(Operation.RENAME, new_key, original.data_ref, **{'from': key})
        # TODO None or actual data ref
        return self._snapshot.apply(log, None)

    def snapshot(self):
        data_object = self._storage.create(list(self._snapshot.keys()))
        log = self._logger.create(Operation.SNAPSHOT, None, data_object.ref)
        return log

    def history(self, key):
        return self._logger.history(key)
