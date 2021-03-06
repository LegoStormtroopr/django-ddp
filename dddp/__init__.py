"""Django/PostgreSQL implementation of the Meteor DDP service."""
from __future__ import unicode_literals
import os.path
import sys
from pkg_resources import get_distribution, DistributionNotFound
from gevent.local import local
from dddp import alea


try:
    _dist = get_distribution('django-ddp')
    if not __file__.startswith(os.path.join(_dist.location, 'django-ddp', '')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'development'
else:
    __version__ = _dist.version

default_app_config = 'dddp.apps.DjangoDDPConfig'

ADDED = 'added'
CHANGED = 'changed'
REMOVED = 'removed'


def greenify():
    """Patch threading and psycopg2 modules for green threads."""
    from gevent.monkey import patch_all, saved
    if ('threading' in sys.modules) and ('threading' not in saved):
        raise Exception('threading module loaded before patching!')
    patch_all()

    from psycogreen.gevent import patch_psycopg
    patch_psycopg()


class AlreadyRegistered(Exception):

    """Raised when registering over the top of an existing registration."""

    pass


class ThreadLocal(local):

    """Thread local storage for greenlet state."""

    _init_done = False

    def __init__(self):
        """Create new thread storage instance."""
        if self._init_done:
            raise SystemError('__init__ called too many times')
        self._init_done = True

    def __getattr__(self, name):
        """Create missing attributes using default factories."""
        try:
            factory = THREAD_LOCAL_FACTORIES[name]
        except KeyError:
            raise AttributeError(name)
        return self.get(name, factory)

    def get(self, name, factory, *factory_args, **factory_kwargs):
        """Get attribute, creating if required using specified factory."""
        update_thread_local = getattr(factory, 'update_thread_local', True)
        if (not update_thread_local) or (not hasattr(self, name)):
            obj = factory(*factory_args, **factory_kwargs)
            if update_thread_local:
                setattr(self, name, obj)
            return obj
        return getattr(self, name)


class RandomStreams(object):

    def __init__(self):
        self._streams = {}
        self._seed = THREAD_LOCAL.alea_random.hex_string(20)

    def get_seed(self):
        return self._seed
    def set_seed(self, val):
        self._streams = {}
        self._seed = val
    random_seed = property(get_seed, set_seed)

    def __getitem__(self, key):
        if key not in self._streams:
            return self._streams.setdefault(key, alea.Alea(self._seed, key))
        return self._streams[key]


def serializer_factory():
    """Make a new DDP serializer."""
    from django.core.serializers import get_serializer
    return get_serializer('python')()


THREAD_LOCAL_FACTORIES = {
    'alea_random': alea.Alea,
    'random_streams': RandomStreams,
    'serializer': serializer_factory,
}
THREAD_LOCAL = ThreadLocal()
METEOR_ID_CHARS = u'23456789ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnopqrstuvwxyz'


def meteor_random_id(name=None, length=17):
    if name is None:
        stream = THREAD_LOCAL.alea_random
    else:
        stream = THREAD_LOCAL.random_streams[name]
    return stream.random_string(length, METEOR_ID_CHARS)


def autodiscover():
    from django.utils.module_loading import autodiscover_modules
    from dddp.api import API
    autodiscover_modules('ddp', register_to=API)
    return API
