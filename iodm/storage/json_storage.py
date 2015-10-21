class ImmutableJsonStorage(Storage):

    def __init__(self, *args, **kwargs):
        self.cache = {}
        self.path = None

        self._is_data_dirty = False
        self._is_tree_dirty = False

        rel_path = kwargs.get('path', None)

        if rel_path:
            self.path = os.path.join(os.path.abspath(rel_path))
            self.data_path = os.path.join(self.path, 'data')
            try:
                os.makedirs(self.data_path)
            except:
                pass

        self.data_storage = ImmutableLocalStorage(path=self.data_path)

        self.key_map = self._get_current_tree()

    def _get_current_tree(self, path=None):
        if not path:
            path = os.path.join(self.path, 'current_tree')
        if os.path.exists(path):
            with open(path, 'r') as fp:
                data_id = fp.read()
            try:
                return self.data_storage.read(data_id)
            except FileNotFoundError:
                raise Exception("Tree does not point to valid data")
        return {}

    def _make_data_path(self, id):
        return os.path.join(self._make_data_directory(id), id[2:])

    def _make_data_directory(self, id):
        return os.path.join(self.data_path, id[0:2])

    def _update_tree(self, key):
        pass

    def _get_data_id(self, key):
        return self.key_map[key]

    def _get_data_by_key(self, key, validate=False):
        data_id = self._get_data_id(key)
        return self.data_storage.read(data_id, validate=validate)

    def _write_data(self, value):
        json_string = json.dumps(value)
        return self.data_storage.write(value)

    def get(self, key, validate=False):
        return self._get_data_by_key(key, validate=validate)

    def set(self, key, value, **kwargs):
        if self.cache.get(key, None) == value:
            return

        self.cache[key] = value
        self._is_data_dirty = True
        if kwargs.get('flush', False):
            self.flush()

    def flush(self):
        for key, value in self.cache.items():
            data_id = self._write_data(value)
            if not self.key_map.get(key, None) == data_id:
                self._is_tree_dirty = True
                self.key_map[key] = data_id

        if self._is_tree_dirty:
            tree_data_id = self._write_data(self.key_map)
            with open(os.path.join(self.path, 'current_tree'), 'w') as fp:
                fp.write(tree_data_id)

        self.cache = {}