import enum

import jsonpatch

import jam
from jam import O
from jam import Q
from jam import exceptions
from jam.schemas import load_schema
from jam.backends.util import load_backend


class Operation(enum.IntEnum):
    CREATE = 0
    UPDATE = 1
    REPLACE = 2
    DELETE = 3
    SNAPSHOT = 4
    RENAME = 5


class ReadOnlyCollection:
    """A Collection interface that only allows reading of data.
    Used for getting specific states in time as past data is not modifiable
    """

    @classmethod
    def from_document(cls, document):
        return cls.from_dict(document.data)

    @staticmethod
    def load_schema(schema):
        return load_schema(schema['type'], schema['schema'])

    @classmethod
    def from_dict(cls, data):
        return cls(
            jam.Storage(load_backend(data['storage']['backend'], **data['storage']['settings'])),
            jam.Logger(load_backend(data['logger']['backend'], **data['logger']['settings'])),
            jam.State(load_backend(data['state']['backend'], **data['state']['settings'])),
            schema=data.get('schema'),
            permissions=data.get('permissions'),
        )

    def __init__(self, storage, logger, state, permissions=None, schema=None):
        self._state = state
        self._logger = logger
        self._storage = storage
        self.permissions = permissions or {}
        if schema:
            schema = self.load_schema(schema)
        self.schema = schema

    # Snapshot interaction

    def regenerate(self):
        # Remove all data otherwise we might have some rogue keys
        self._state.clear()

        try:
            snapshot_log = self._logger.latest_snapshot()
        except exceptions.NotFound:
            # Otherwise apply all logs
            logs = list(self._logger.list(O('modified_on', O.ASCENDING)))
        else:
            # If we've found the snap shot, load it and apply all logs after it
            self.load_snapshot(snapshot_log)
            # Note: After sorts ascending on timestamp
            logs = list(self._logger.after(snapshot_log.modified_on))

        data_objects = {}
        for data_object in self._storage._backend.query(Q('ref', 'in', [
            log.data_ref for log in logs if log.data_ref
        ])):
            data_objects[data_object.ref] = data_object

        acc = 0
        for log in logs:
            acc += 1
            self._state.apply(log, log.data_ref and data_objects[log.data_ref].data)

        return acc  # The number of logs that were not included from the snapshot

    def load_snapshot(self, snapshot_log):
        # Pull our data object, a list of log refs
        data_object = self._storage.get(snapshot_log.data_ref)
        logs, data_objects = zip(*data_object.data)

        log_map = {log.ref: log for log in self._logger.bulk_read(logs)}
        data_object_map = {do.ref: do for do in self._storage.bulk_read(data_objects)}

        # Load and apply each log ref
        for log, data_object in zip(logs, data_objects):
            self._state.apply(log_map[log], data_object_map[data_object].data, safe=False)

    # Data interaction

    def select(self):
        return self._state._backend.select()

    def list(self):
        return self._state.list()

    def keys(self):
        return self._state.keys()

    def read(self, key):
        try:
            doc = self._state.get(key)
            if doc.data is None and doc.data_ref:
                doc.data = self._storage.get(doc.data_ref)
            return doc
        except exceptions.NotFound:
            raise exceptions.NotFound(
                code='D404',
                title='Document not found',
                detail='Document "{}" was not found'.format(key)
            )

    def history(self, key):
        return self._logger.history(key)

    def __repr__(self):
        return '<{}({}, {}, {})>'.format(self.__class__.__name__, self._storage, self._logger, self._state)


class FrozenCollection(ReadOnlyCollection):

    def snapshot(self):
        data_object = self._storage.create([(doc.log_ref, doc.data_ref) for doc in self._state.list()])
        log = self._logger.create_snapshot(data_object.ref)
        return log


class BaseCollection(ReadOnlyCollection):

    def snapshot(self):
        data_object = self._storage.create([(doc.log_ref, doc.data_ref) for doc in self._state.list()])
        log = self._logger.create(None, Operation.SNAPSHOT, data_object.ref, None)
        return log

    def create(self, key, data, user):
        if self.schema:
            self.schema.validate(data)

        try:
            self._state.get(key)
        except exceptions.NotFound:
            pass
        else:
            raise exceptions.KeyExists(
                code='D409',
                title='Document already exists',
                detail='Document "{}" already exists'.format(key)
            )

        data_object = self._storage.create(data)

        return self._state.apply(self._logger.create(
            key,
            Operation.CREATE,
            data_object.ref,
            user
        ), data)

    def update(self, key, patch, user):
        previous = self._state.get(key)

        if isinstance(patch, dict):
            patch = self._generate_patch(previous.data, patch)

        patch = self._validate_patch(patch)
        schema_updates = [p for p in patch if p['path'] == '/schema' and p['op'] != 'remove']
        for update in schema_updates:
            # ensure new schema(s) are valid
            self.load_schema(update['value'])

        try:
            data = jsonpatch.apply_patch(previous.data, patch)
        except jsonpatch.JsonPatchTestFailed as e:
            raise exceptions.JsonPatchTestFailed(e)

        if self.schema:
            self.schema.validate(data)

        data_object = self._storage.create(data)

        return self._state.apply(self._logger.create(
            key,
            Operation.UPDATE,
            data_object.ref,
            user,
            previous=previous,
            operation_parameters={'patch': list(patch)}
        ), data)

    # TODO
    def replace(self, key, data, user):
        previous = self._state.get(key)

        if self.schema:
            self.schema.validate(data)

        data_object = self._storage.create(data)

        return self._state.apply(self._logger.create(
            key,
            Operation.UPDATE,
            data_object.ref,
            user,
            previous=previous,
        ), data)

    def delete(self, key, user):
        # data_ref for delete logs should always be None
        previous = self._state.get(key)
        return self._state.apply(self._logger.create(
            key,
            Operation.DELETE,
            None,
            user,
            previous=previous
        ), None)

    def rename(self, key, new_key, user):
        # Create two logs, one for the from key, effectively a delete
        # and another for the to key, effectively a create
        previous = self._state.get(key)
        self._state.apply(self._logger.create(
            key,
            Operation.RENAME,
            None,
            user,
            previous=previous,
            operation_parameters={'to': new_key}
        ), None)

        return self._state.apply(self._logger.create(
            new_key,
            Operation.RENAME,
            previous.data_ref,
            user,
            previous=previous,
            operation_parameters={'from': key}
        ), previous.data)

    def at_time(self, timestamp, state, regenerate=True):
        """Given a unix timestamp and a state (Should be empty)
        creates a ReadOnlyCollection for this collection at that point in time.
        Note: The closer timestamp is to a saved state the faster this will be
        """
        frozen = FrozenCollection(
            self._storage,
            self._logger.at_time(timestamp),
            state,
            # Note: No need to pass in schema, read-only collections have no use for it
            permissions=self.permissions
        )
        if regenerate:
            frozen.regenerate()
        return frozen

    def _generate_patch(self, previous, new):
        return jsonpatch.JsonPatch.from_diff(previous, new)

    def _validate_patch(self, patch):
        return patch
