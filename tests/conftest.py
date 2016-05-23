from jam import settings
# Hack to force all storages into memory
settings.load('test.yml', local=True)
settings.load('test-local.yml', local=True, _try=True)

import pytest

import datetime
import random
import string
import time
import types

from freezegun import freeze_time

from jam.backends.util import get_backends
from jam.logger import Logger
from jam.logger import ReadOnlyLogger
from jam.models import DataObject
from jam.state import State
from jam.storage import ReadOnlyStorage
from jam.storage import Storage


rndstr = lambda a, b: ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(a, b)))


def gendata(length):
    return tuple(
        DataObject(
            ref=rndstr(5, 20),
            data={
                rndstr(5, 20): rndstr(0, 25)
                for _ in range(random.randint(0, 25))
            }
        )
        for _ in range(length)
    )


available_backends = [backend for backend in get_backends() if backend.is_connected()]
backend_fixture = pytest.yield_fixture(params=available_backends, ids=[backend.__name__ for backend in available_backends])


def _backend(request):
    backend = request.param
    request.applymarker(getattr(pytest.mark, backend.__name__)())
    inst = backend(**backend.settings_for('test', 'test', request.fixturename))
    yield inst
    inst.unset_all()


def backend():
    return types.FunctionType(
        _backend.__code__,
        _backend.__globals__,
        name=_backend.__name__,
        closure=_backend.__closure__,
        argdefs=_backend.__defaults__,
    )


state_backend = backend()
logger_backend = backend()
storage_backend = backend()

pytest.yield_fixture(
    params=available_backends,
    ids=[b.__name__.replace('Backend', 'State') for b in available_backends]
)(state_backend)

pytest.yield_fixture(
    params=available_backends,
    ids=[b.__name__.replace('Backend', 'Logger') for b in available_backends]
)(logger_backend)

pytest.yield_fixture(
    params=available_backends,
    ids=[b.__name__.replace('Backend', 'Storage') for b in available_backends]
)(storage_backend)


@pytest.yield_fixture
def freezetime():
    ftime = datetime.datetime.now()
    offset = (-time.timezone // 3600)
    # og_time = time.time.__class__.__call__
    freezer = freeze_time(ftime, tz_offset=offset)
    freezer.start()
    time.time.__class__.__call__ = lambda self: self.time_to_freeze().timestamp()
    yield freezer
    # time.time.__class__.__class__ = og_time
    freezer.stop()


_sampledata = (
    (DataObject(ref='empty', data={}),),
    (
        DataObject(ref='empty', data={}),
        DataObject(ref='empty2', data={}),
    ),
    (
        DataObject(ref='empty', data={}),
        DataObject(ref='empty2', data={}),
        DataObject(ref='empty3', data={}),
    ),
    (
        DataObject(ref='empty', data={}),
        DataObject(ref='empty2', data={}),
        DataObject(ref='empty3', data={}),
        DataObject(ref='empty4', data={}),
    ),
    gendata(10),
    gendata(20),
    gendata(30),
    gendata(40),
    gendata(50),
)


@pytest.fixture(params=_sampledata)
def sampledata(request):
    return request.param


@pytest.fixture
def logger(logger_backend):
    return Logger(logger_backend)


@pytest.fixture
def readonlylogger(logger_backend):
    return ReadOnlyLogger(logger_backend)


@pytest.fixture
def storage(storage_backend):
    return Storage(storage_backend)


@pytest.fixture
def readonlystorage(storage_backend):
    return ReadOnlyStorage(storage_backend)


@pytest.fixture
def state(state_backend):
    return State(state_backend)
