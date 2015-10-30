from iodm import O
from iodm.base import Operation
from iodm.storage import ReadOnlyStorage


class ReadOnlyCollection:
    """A Collection interface that only allows reading of data.
    Used for getting specific states in time as past data is not modifiable
    """

    def __init__(self, storage, logger, snapshot, regenerate=True):
        self._logger = logger
        self._storage = storage
        self._snapshot = snapshot
        if regenerate:
            # Snapshot will get overwritten here if it is not empty
            # A new snapshot cannot be generated as we have no idea what parameters to pass it
            self.regenerate()

    # Snapshot interaction

    def regenerate(self):
        # Remove all data otherwise we might have some rogue keys
        self._snapshot.clear()

        snapshot_log = self._logger.latest_snapshot()

        if snapshot_log:
            # If we've found the snap shot, load it and apply all logs after it
            self.load_snapshot(snapshot_log)
            # Note: After sorts ascending on timestamp
            logs = self._logger.after(snapshot_log.timestamp)
        else:
            # Otherwise apply all logs
            logs = self._logger.list(O('timestamp', O.ASCENDING))

        for log in logs:
            self._snapshot.apply(log)

        return True

    def load_snapshot(self, snapshot_log):
        # Pull our data object, a list of log refs
        data_object = self._storage.get(snapshot_log.data_ref)

        # Load and apply each log ref
        for log_ref in data_object.data:
            self._snapshot.apply(self._logger.get(log_ref), safe=False)

    # Data interaction

    def list(self):
        return self._snapshot.list()

    def read(self, key):
        return self._storage.get(self._snapshot.get(key).data_ref)

    def history(self, key):
        return self._logger.history(key)


class Collection(ReadOnlyCollection):

    def snapshot(self):
        data_object = self._storage.create([log.ref for log in self._snapshot.list()])
        log = self._logger.create(Operation.SNAPSHOT, None, data_object.ref)
        return log

    def create(self, key, data):
        data_object = self._storage.create(data)
        log = self._logger.create(Operation.CREATE, key, data_object.ref)
        return self._snapshot.apply(log)

    def update(self, key, data, merger=None):
        if merger:
            original = self._snapshot.get(key)
            data = merger(original, data)
        data_object = self._storage.create(data)
        log = self._logger.create(Operation.UPDATE, key, data_object.ref)
        return self._snapshot.apply(log)

    def delete(self, key):
        # data_ref for delete logs should always be None
        log = self._logger.create(Operation.DELETE, key, None)
        return self._snapshot.apply(log)

    def rename(self, key, new_key):
        # Create two logs, one for the from key, effectively a delete
        # and another for the to key, effectively a create
        original = self._snapshot.get(key)
        log = self._logger.create(Operation.RENAME, key, None, **{'to': new_key})
        self._snapshot.apply(log)

        log = self._logger.create(Operation.RENAME, new_key, original.data_ref, **{'from': key})
        return self._snapshot.apply(log)

    def at_time(self, timestamp, snapshot):
        """Given a unix timestamp and a snapshot (Should be empty)
        creates a ReadOnlyCollection for this collection at that point in time.
        Note: The closer timestamp is to a saved snapshot the faster this will be
        """
        return ReadOnlyCollection(
            # This feels a bit odd, need a better interface unwrapping backends
            # Unwraps storages backend to the raw backend, the input expected by ReadOnlyStorage
            ReadOnlyStorage(self._storage._backend._backend),
            self._logger.at_time(timestamp),
            snapshot,
            regenerate=True
        )
