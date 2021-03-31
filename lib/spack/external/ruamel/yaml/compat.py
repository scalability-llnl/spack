# coding: utf-8

from __future__ import print_function

# partially from package six by Benjamin Peterson

import sys
import os
import types

try:
    from ruamel.ordereddict import ordereddict
except:
    try:
        from collections.abc import OrderedDict
    except ImportError:
        try:
            from collections import OrderedDict
        except ImportError:
            from ordereddict import OrderedDict

    # Monkey-patch `ordereddict.insert()` for very old Python versions.
    class ordereddict(OrderedDict):
        if not hasattr(OrderedDict, 'insert'):
            def insert(self, pos, key, value):
                if pos >= len(self):
                    self[key] = value
                    return
                od = ordereddict()
                od.update(self)
                for k in od:
                    del self[k]
                for index, old_key in enumerate(od):
                    if pos == index:
                        self[key] = value
                    self[old_key] = od[old_key]


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    def utf8(s):
        return s

    def to_str(s):
        return s

    def to_unicode(s):
        return s

else:
    def utf8(s):
        return s.encode('utf-8')

    def to_str(s):
        return str(s)

    def to_unicode(s):
        return unicode(s)

if PY3:
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes

    MAXSIZE = sys.maxsize
    unichr = chr
    import io
    StringIO = io.StringIO
    BytesIO = io.BytesIO

else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str

    unichr = unichr  # to allow importing
    import StringIO
    StringIO = StringIO.StringIO
    import cStringIO
    BytesIO = cStringIO.StringIO

if PY3:
    builtins_module = 'builtins'
else:
    builtins_module = '__builtin__'


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    return meta("NewBase", bases, {})

DBG_TOKEN = 1
DBG_EVENT = 2
DBG_NODE = 4


_debug = None


# used from yaml util when testing
def dbg(val=None):
    global _debug
    if _debug is None:
        # set to true or false
        _debug = os.environ.get('YAMLDEBUG')
        if _debug is None:
            _debug = 0
        else:
            _debug = int(_debug)
    if val is None:
        return _debug
    return _debug & val


def nprint(*args, **kw):
    if dbg:
        print(*args, **kw)
