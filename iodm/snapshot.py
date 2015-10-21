class Snapshot():
    def __init__(self, *args, **kwargs):
        self.cache = {}

    def get_hash(self, key):
        return self.cache[key]

    def create(self, key, hash_string):
        self.cache[key] = hash_string

    def update(self, key, hash_string):
        self.cache[key] = hash_string

    def rename(self, old, new):
        self.cache[new] = self.cache[old]
        del self.cache[old]

    def remove(self, key):
        del self.cache[key]

    def get(self):
        pass

    def build_from_snapshot(self):
        pass

    def build_from_log(self, log):
        pass