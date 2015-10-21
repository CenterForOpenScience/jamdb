import bson
import hashlib

def get_checksum(fp, algo=hashlib.md5, read=8096):
    # if float(filesize) == 0:
        # return None
    m = algo()
    while True :
        d = fp.read(read)
        if not d:
            break
        try:
            m.update(d)
        except TypeError: # specifically "Unicode-objects must be encoded before hashing"
            # TODO optimal?
            m.update(d.encode('utf-8'))
    return m.hexdigest()

def generate_id():
    return str(bson.ObjectId())[::-1]