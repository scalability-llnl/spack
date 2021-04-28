# coding: utf-8

from __future__ import absolute_import

__all__ = ['BaseLoader', 'SafeLoader', 'Loader', 'RoundTripLoader']

try:
    from .reader import *                                # NOQA
    from .scanner import *                               # NOQA
    from .parser import *                                # NOQA
    from .composer import *                              # NOQA
    from .constructor import *                           # NOQA
    from .resolver import *                              # NOQA
except (ImportError, ValueError):  # for Jython
    from ruamel.yaml.reader import *                                # NOQA
    from ruamel.yaml.scanner import *                               # NOQA
    from ruamel.yaml.parser import *                                # NOQA
    from ruamel.yaml.composer import *                              # NOQA
    from ruamel.yaml.constructor import *                           # NOQA
    from ruamel.yaml.resolver import *                              # NOQA


class BaseLoader(Reader, Scanner, Parser, Composer, BaseConstructor, BaseResolver):
    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        BaseConstructor.__init__(self)
        BaseResolver.__init__(self)


class SafeLoader(Reader, Scanner, Parser, Composer, SafeConstructor, Resolver):
    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        SafeConstructor.__init__(self)
        Resolver.__init__(self)


class Loader(Reader, Scanner, Parser, Composer, Constructor, VersionedResolver):
    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        Constructor.__init__(self)
        VersionedResolver.__init__(self)


class RoundTripLoader(Reader, RoundTripScanner, RoundTripParser, Composer,
                      RoundTripConstructor, VersionedResolver):
    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        RoundTripScanner.__init__(self)
        RoundTripParser.__init__(self)
        Composer.__init__(self)
        RoundTripConstructor.__init__(self, preserve_quotes=preserve_quotes)
        VersionedResolver.__init__(self, version)
