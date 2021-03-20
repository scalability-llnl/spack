# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import division

import multiprocessing
import os
import re
import functools
import inspect
import sys
from datetime import datetime, timedelta
from six import string_types
from typing import Callable, TypeVar


if sys.version_info >= (3, 3):
    from collections.abc import MutableMapping  # novm
else:
    from collections import MutableMapping


# Ignore emacs backups when listing modules
ignore_modules = [r'^\.#', '~$']


# On macOS, Python 3.8 multiprocessing now defaults to the 'spawn' start
# method. Spack cannot currently handle this, so force the process to start
# using the 'fork' start method.
#
# TODO: This solution is not ideal, as the 'fork' start method can lead to
# crashes of the subprocess. Figure out how to make 'spawn' work.
#
# See:
# * https://github.com/spack/spack/pull/18124
# * https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods  # noqa: E501
# * https://bugs.python.org/issue33725
if sys.version_info >= (3,):  # novm
    fork_context = multiprocessing.get_context('fork')
else:
    fork_context = multiprocessing


def index_by(objects, *funcs):
    """Create a hierarchy of dictionaries by splitting the supplied
    set of objects on unique values of the supplied functions.

    Values are used as keys. For example, suppose you have four
    objects with attributes that look like this::

        a = Spec("boost %gcc target=skylake")
        b = Spec("mrnet %intel target=zen2")
        c = Spec("libelf %xlc target=skylake")
        d = Spec("libdwarf %intel target=zen2")

        list_of_specs = [a,b,c,d]
        index1 = index_by(list_of_specs, lambda s: str(s.target),
                          lambda s: s.compiler)
        index2 = index_by(list_of_specs, lambda s: s.compiler)

    ``index1`` now has two levels of dicts, with lists at the
    leaves, like this::

        { 'zen2'    : { 'gcc' : [a], 'xlc' : [c] },
          'skylake' : { 'intel' : [b, d] }
        }

    And ``index2`` is a single level dictionary of lists that looks
    like this::

        { 'gcc'    : [a],
          'intel'  : [b,d],
          'xlc'    : [c]
        }

    If any elements in funcs is a string, it is treated as the name
    of an attribute, and acts like getattr(object, name).  So
    shorthand for the above two indexes would be::

        index1 = index_by(list_of_specs, 'arch', 'compiler')
        index2 = index_by(list_of_specs, 'compiler')

    You can also index by tuples by passing tuples::

        index1 = index_by(list_of_specs, ('target', 'compiler'))

    Keys in the resulting dict will look like ('gcc', 'skylake').
    """
    if not funcs:
        return objects

    f = funcs[0]
    if isinstance(f, str):
        f = lambda x: getattr(x, funcs[0])
    elif isinstance(f, tuple):
        f = lambda x: tuple(getattr(x, p) for p in funcs[0])

    result = {}
    for o in objects:
        key = f(o)
        result.setdefault(key, []).append(o)

    for key, objects in result.items():
        result[key] = index_by(objects, *funcs[1:])

    return result


def caller_locals():
    """This will return the locals of the *parent* of the caller.
       This allows a function to insert variables into its caller's
       scope.  Yes, this is some black magic, and yes it's useful
       for implementing things like depends_on and provides.
    """
    # Passing zero here skips line context for speed.
    stack = inspect.stack(0)
    try:
        return stack[2][0].f_locals
    finally:
        del stack


def get_calling_module_name():
    """Make sure that the caller is a class definition, and return the
       enclosing module's name.
    """
    # Passing zero here skips line context for speed.
    stack = inspect.stack(0)
    try:
        # Make sure locals contain __module__
        caller_locals = stack[2][0].f_locals
    finally:
        del stack

    if '__module__' not in caller_locals:
        raise RuntimeError("Must invoke get_calling_module_name() "
                           "from inside a class definition!")

    module_name = caller_locals['__module__']
    base_name = module_name.split('.')[-1]
    return base_name


def attr_required(obj, attr_name):
    """Ensure that a class has a required attribute."""
    if not hasattr(obj, attr_name):
        raise RequiredAttributeError(
            "No required attribute '%s' in class '%s'"
            % (attr_name, obj.__class__.__name__))


def attr_setdefault(obj, name, value):
    """Like dict.setdefault, but for objects."""
    if not hasattr(obj, name):
        setattr(obj, name, value)
    return getattr(obj, name)


def has_method(cls, name):
    for base in inspect.getmro(cls):
        if base is object:
            continue
        if name in base.__dict__:
            return True
    return False


def union_dicts(*dicts):
    """Use update() to combine all dicts into one.

    This builds a new dictionary, into which we ``update()`` each element
    of ``dicts`` in order.  Items from later dictionaries will override
    items from earlier dictionaries.

    Args:
        dicts (list): list of dictionaries

    Return: (dict): a merged dictionary containing combined keys and
        values from ``dicts``.

    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


_F = TypeVar('_F', bound=Callable)


def memoized(func):
    # type: (_F) -> _F
    """Decorator that caches the results of a function, storing them in
    an attribute of that function.
    """
    func.cache = {}  # type: ignore[attr-defined]

    @functools.wraps(func)
    def _memoized_function(*args, **kwargs):
        assert isinstance(args, tuple), args
        key = args + tuple(kwargs.items() if kwargs else [])

        try:
            ret = func.cache[key]
        except KeyError:
            ret = func(*args, **kwargs)
            func.cache[key] = ret
        except TypeError:
            # Not hashable, so just call the function.
            ret = func(*args, **kwargs)
        return ret

    return _memoized_function  # type: ignore[return-value]


def list_modules(directory, **kwargs):
    """Lists all of the modules, excluding ``__init__.py``, in a
       particular directory.  Listed packages have no particular
       order."""
    list_directories = kwargs.setdefault('directories', True)

    for name in os.listdir(directory):
        if name == '__init__.py':
            continue

        path = os.path.join(directory, name)
        if list_directories and os.path.isdir(path):
            init_py = os.path.join(path, '__init__.py')
            if os.path.isfile(init_py):
                yield name

        elif name.endswith('.py'):
            if not any(re.search(pattern, name) for pattern in ignore_modules):
                yield re.sub('.py$', '', name)


def key_ordering(cls):
    """Decorates a class with extra methods that implement rich comparison
       operations and ``__hash__``.  The decorator assumes that the class
       implements a function called ``_cmp_key()``.  The rich comparison
       operations will compare objects using this key, and the ``__hash__``
       function will return the hash of this key.

       If a class already has ``__eq__``, ``__ne__``, ``__lt__``, ``__le__``,
       ``__gt__``, or ``__ge__`` defined, this decorator will overwrite them.

       Raises:
           TypeError: If the class does not have a ``_cmp_key`` method
    """
    def setter(name, value):
        value.__name__ = name
        setattr(cls, name, value)

    if not has_method(cls, '_cmp_key'):
        raise TypeError("'%s' doesn't define _cmp_key()." % cls.__name__)

    setter('__eq__',
           lambda s, o:
           (s is o) or (o is not None and s._cmp_key() == o._cmp_key()))
    setter('__lt__',
           lambda s, o: o is not None and s._cmp_key() < o._cmp_key())
    setter('__le__',
           lambda s, o: o is not None and s._cmp_key() <= o._cmp_key())

    setter('__ne__',
           lambda s, o:
           (s is not o) and (o is None or s._cmp_key() != o._cmp_key()))
    setter('__gt__',
           lambda s, o: o is None or s._cmp_key() > o._cmp_key())
    setter('__ge__',
           lambda s, o: o is None or s._cmp_key() >= o._cmp_key())

    setter('__hash__', lambda self: hash(self._cmp_key()))

    return cls


@key_ordering
class HashableMap(MutableMapping):
    """This is a hashable, comparable dictionary.  Hash is performed on
       a tuple of the values in the dictionary."""

    def __init__(self):
        self.dict = {}

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __iter__(self):
        return iter(self.dict)

    def __len__(self):
        return len(self.dict)

    def __delitem__(self, key):
        del self.dict[key]

    def _cmp_key(self):
        return tuple(sorted(self.values()))

    def copy(self):
        """Type-agnostic clone method.  Preserves subclass type."""
        # Construct a new dict of my type
        self_type = type(self)
        clone = self_type()

        # Copy everything from this dict into it.
        for key in self:
            clone[key] = self[key].copy()
        return clone


def in_function(function_name):
    """True if the caller was called from some function with
       the supplied Name, False otherwise."""
    stack = inspect.stack()
    try:
        for elt in stack[2:]:
            if elt[3] == function_name:
                return True
        return False
    finally:
        del stack


def check_kwargs(kwargs, fun):
    """Helper for making functions with kwargs.  Checks whether the kwargs
       are empty after all of them have been popped off.  If they're
       not, raises an error describing which kwargs are invalid.

       Example::

          def foo(self, **kwargs):
              x = kwargs.pop('x', None)
              y = kwargs.pop('y', None)
              z = kwargs.pop('z', None)
              check_kwargs(kwargs, self.foo)

          # This raises a TypeError:
          foo(w='bad kwarg')
    """
    if kwargs:
        raise TypeError(
            "'%s' is an invalid keyword argument for function %s()."
            % (next(iter(kwargs)), fun.__name__))


def match_predicate(*args):
    """Utility function for making string matching predicates.

    Each arg can be a:
    * regex
    * list or tuple of regexes
    * predicate that takes a string.

    This returns a predicate that is true if:
    * any arg regex matches
    * any regex in a list or tuple of regexes matches.
    * any predicate in args matches.
    """
    def match(string):
        for arg in args:
            if isinstance(arg, string_types):
                if re.search(arg, string):
                    return True
            elif isinstance(arg, list) or isinstance(arg, tuple):
                if any(re.search(i, string) for i in arg):
                    return True
            elif callable(arg):
                if arg(string):
                    return True
            else:
                raise ValueError("args to match_predicate must be regex, "
                                 "list of regexes, or callable.")
        return False
    return match


def dedupe(sequence):
    """Yields a stable de-duplication of an hashable sequence

    Args:
        sequence: hashable sequence to be de-duplicated

    Returns:
        stable de-duplication of the sequence
    """
    seen = set()
    for x in sequence:
        if x not in seen:
            yield x
            seen.add(x)


def pretty_date(time, now=None):
    """Convert a datetime or timestamp to a pretty, relative date.

    Args:
        time (datetime or int): date to print prettily
        now (datetime): dateimte for 'now', i.e. the date the pretty date
            is relative to (default is datetime.now())

    Returns:
        (str): pretty string like 'an hour ago', 'Yesterday',
            '3 months ago', 'just now', etc.

    Adapted from https://stackoverflow.com/questions/1551382.

    """
    if now is None:
        now = datetime.now()

    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    else:
        raise ValueError("pretty_date requires a timestamp or datetime")

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 28:
        weeks = day_diff // 7
        if weeks == 1:
            return "a week ago"
        else:
            return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        months = day_diff // 30
        if months == 1:
            return "a month ago"
        elif months == 12:
            months -= 1
        return str(months) + " months ago"

    diff = day_diff // 365
    if diff == 1:
        return "a year ago"
    else:
        return str(diff) + " years ago"


def pretty_string_to_date(date_str, now=None):
    """Parses a string representing a date and returns a datetime object.

    Args:
        date_str (str): string representing a date. This string might be
            in different format (like ``YYYY``, ``YYYY-MM``, ``YYYY-MM-DD``,
            ``YYYY-MM-DD HH:MM``, ``YYYY-MM-DD HH:MM:SS``)
            or be a *pretty date* (like ``yesterday`` or ``two months ago``)

    Returns:
        (datetime): datetime object corresponding to ``date_str``
    """

    pattern = {}

    now = now or datetime.now()

    # datetime formats
    pattern[re.compile(r'^\d{4}$')] = lambda x: datetime.strptime(x, '%Y')
    pattern[re.compile(r'^\d{4}-\d{2}$')] = lambda x: datetime.strptime(
        x, '%Y-%m'
    )
    pattern[re.compile(r'^\d{4}-\d{2}-\d{2}$')] = lambda x: datetime.strptime(
        x, '%Y-%m-%d'
    )
    pattern[re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$')] = \
        lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M')
    pattern[re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')] = \
        lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    pretty_regex = re.compile(
        r'(a|\d+)\s*(year|month|week|day|hour|minute|second)s?\s*ago')

    def _n_xxx_ago(x):
        how_many, time_period = pretty_regex.search(x).groups()

        how_many = 1 if how_many == 'a' else int(how_many)

        # timedelta natively supports time periods up to 'weeks'.
        # To apply month or year we convert to 30 and 365 days
        if time_period == 'month':
            how_many *= 30
            time_period = 'day'
        elif time_period == 'year':
            how_many *= 365
            time_period = 'day'

        kwargs = {(time_period + 's'): how_many}
        return now - timedelta(**kwargs)

    pattern[pretty_regex] = _n_xxx_ago

    # yesterday
    callback = lambda x: now - timedelta(days=1)
    pattern[re.compile('^yesterday$')] = callback

    for regexp, parser in pattern.items():
        if bool(regexp.match(date_str)):
            return parser(date_str)

    msg = 'date "{0}" does not match any valid format'.format(date_str)
    raise ValueError(msg)


class RequiredAttributeError(ValueError):

    def __init__(self, message):
        super(RequiredAttributeError, self).__init__(message)


class ObjectWrapper(object):
    """Base class that wraps an object. Derived classes can add new behavior
    while staying undercover.

    This class is modeled after the stackoverflow answer:
    * http://stackoverflow.com/a/1445289/771663
    """
    def __init__(self, wrapped_object):
        wrapped_cls = type(wrapped_object)
        wrapped_name = wrapped_cls.__name__

        # If the wrapped object is already an ObjectWrapper, or a derived class
        # of it, adding type(self) in front of type(wrapped_object)
        # results in an inconsistent MRO.
        #
        # TODO: the implementation below doesn't account for the case where we
        # TODO: have different base classes of ObjectWrapper, say A and B, and
        # TODO: we want to wrap an instance of A with B.
        if type(self) not in wrapped_cls.__mro__:
            self.__class__ = type(wrapped_name, (type(self), wrapped_cls), {})
        else:
            self.__class__ = type(wrapped_name, (wrapped_cls,), {})

        self.__dict__ = wrapped_object.__dict__


class Singleton(object):
    """Simple wrapper for lazily initialized singleton objects."""

    def __init__(self, factory):
        """Create a new singleton to be inited with the factory function.

        Args:
            factory (function): function taking no arguments that
                creates the singleton instance.
        """
        self.factory = factory
        self._instance = None

    @property
    def instance(self):
        if self._instance is None:
            self._instance = self.factory()
        return self._instance

    def __getattr__(self, name):
        # When unpickling Singleton objects, the 'instance' attribute may be
        # requested but not yet set. The final 'getattr' line here requires
        # 'instance'/'_instance' to be defined or it will enter an infinite
        # loop, so protect against that here.
        if name in ['_instance', 'instance']:
            raise AttributeError()
        return getattr(self.instance, name)

    def __getitem__(self, name):
        return self.instance[name]

    def __contains__(self, element):
        return element in self.instance

    def __call__(self, *args, **kwargs):
        return self.instance(*args, **kwargs)

    def __iter__(self):
        return iter(self.instance)

    def __str__(self):
        return str(self.instance)

    def __repr__(self):
        return repr(self.instance)


class LazyReference(object):
    """Lazily evaluated reference to part of a singleton."""

    def __init__(self, ref_function):
        self.ref_function = ref_function

    def __getattr__(self, name):
        if name == 'ref_function':
            raise AttributeError()
        return getattr(self.ref_function(), name)

    def __getitem__(self, name):
        return self.ref_function()[name]

    def __str__(self):
        return str(self.ref_function())

    def __repr__(self):
        return repr(self.ref_function())


def load_module_from_file(module_name, module_path):
    """Loads a python module from the path of the corresponding file.

    Args:
        module_name (str): namespace where the python module will be loaded,
            e.g. ``foo.bar``
        module_path (str): path of the python file containing the module

    Returns:
        A valid module object

    Raises:
        ImportError: when the module can't be loaded
        FileNotFoundError: when module_path doesn't exist
    """
    if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
        import importlib.util
        spec = importlib.util.spec_from_file_location(  # novm
            module_name, module_path)
        module = importlib.util.module_from_spec(spec)  # novm
        spec.loader.exec_module(module)
    elif sys.version_info[0] == 3 and sys.version_info[1] < 5:
        import importlib.machinery
        loader = importlib.machinery.SourceFileLoader(  # novm
            module_name, module_path)
        module = loader.load_module()
    elif sys.version_info[0] == 2:
        import imp
        module = imp.load_source(module_name, module_path)
    return module


def uniq(sequence):
    """Remove strings of duplicate elements from a list.

    This works like the command-line ``uniq`` tool.  It filters strings
    of duplicate elements in a list. Adjacent matching elements are
    merged into the first occurrence.

    For example::

        uniq([1, 1, 1, 1, 2, 2, 2, 3, 3]) == [1, 2, 3]
        uniq([1, 1, 1, 1, 2, 2, 2, 1, 1]) == [1, 2, 1]

    """
    if not sequence:
        return []

    uniq_list = [sequence[0]]
    last = sequence[0]
    for element in sequence[1:]:
        if element != last:
            uniq_list.append(element)
            last = element
    return uniq_list


def star(func):
    """Unpacks arguments for use with Multiprocessing mapping functions"""
    def _wrapper(args):
        return func(*args)
    return _wrapper


class Devnull(object):
    """Null stream with less overhead than ``os.devnull``.

    See https://stackoverflow.com/a/2929954.
    """
    def write(self, *_):
        pass
