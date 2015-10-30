import calendar
import datetime

from freezegun import freeze_time

from iodm import Logger
from iodm import Storage
from iodm import Snapshot
from iodm import Collection
from iodm.backends import EphemeralBackend


if __name__ == '__main__':
    logger = Logger(EphemeralBackend())
    storage = Storage(EphemeralBackend())
    snapshot = Snapshot(EphemeralBackend())
    collection = Collection(storage, logger, snapshot, regenerate=False)

    ts2012 = calendar.timegm(datetime.datetime(year=2012, month=1, day=14).timetuple())
    ts2013 = calendar.timegm(datetime.datetime(year=2013, month=1, day=14).timetuple())
    ts2014 = calendar.timegm(datetime.datetime(year=2014, month=1, day=14).timetuple())

    with freeze_time('2012-01-14'):
        collection.create('key1', 'value20120114')

    with freeze_time('2013-01-14'):
        collection.create('key1', 'value20130114')

    with freeze_time('2014-01-14'):
        collection.create('key1', 'value20140114')
        collection.create('2014key', 'value')

    frozen = collection.at_time(ts2012, Snapshot(EphemeralBackend()))
    assert frozen.read('key1').data == 'value20120114'
    try:
        key = frozen.read('2014key')
    except Exception:
        key = None

    assert key is None

    frozen = collection.at_time(ts2014, Snapshot(EphemeralBackend()))
    assert frozen.read('key1').data == 'value20140114'
    assert frozen.read('2014key').data == 'value'

    frozen = collection.at_time(ts2013, Snapshot(EphemeralBackend()))
    assert frozen.read('key1').data == 'value20130114'
    try:
        key = frozen.read('2014key')
    except Exception:
        key = None

    assert key is None
