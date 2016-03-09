import hashlib
import collections

import ujson as json


def order_dictionary(dict_obj):
    ordered = collections.OrderedDict()
    for key in sorted(dict_obj.keys()):
        if isinstance(dict_obj[key], dict):
            ordered[key] = order_dictionary(dict_obj[key])
        else:
            ordered[key] = dict_obj[key]
    return ordered


def hash_dictionary(dict_obj, alg='sha1'):
    hasher = hashlib.new(alg)
    hasher.update(json.dumps(order_dictionary(dict_obj)).encode('utf-8'))
    return hasher.hexdigest()
