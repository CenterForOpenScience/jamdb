
class FileStorage(Storage):

    def __init__(self, location):
        self.location = location
        os.makedirs(location, exist_ok=True)

    def create(self, data_object):
        prefix, postfix = data_object.ref[:2], data_object.ref[2:]

        path = os.path.join(self.location, prefix)
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, postfix)

        with open(path, 'w') as fileobj:
            fileobj.write(json.dumps(data_object._asdict()))
        return data_object

    def read(self, key):
        path = os.path.join(self.location, key[:2], key[2:])

        with open(path) as fileobj:
            return DataObject(**json.load(fileobj))

    def keys(self):
        files = list(os.scandir(self.location))
        while files:
            cur = files.pop(0)
            if cur.is_file():
                yield ''.join(cur.path.split('/')[-2:])
            else:
                files.extend(list(os.scandir(cur.path)))
