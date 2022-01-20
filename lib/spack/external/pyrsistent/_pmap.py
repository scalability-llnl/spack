from ._compat import Mapping, Hashable
from itertools import chain
import six
from pyrsistent._pvector import pvector
from pyrsistent._transformations import transform


class PMap(object):
    """
    Persistent map/dict. Tries to follow the same naming conventions as the built in dict where feasible.

    Do not instantiate directly, instead use the factory functions :py:func:`m` or :py:func:`pmap` to
    create an instance.

    Was originally written as a very close copy of the Clojure equivalent but was later rewritten to closer
    re-assemble the python dict. This means that a sparse vector (a PVector) of buckets is used. The keys are
    hashed and the elements inserted at position hash % len(bucket_vector). Whenever the map size exceeds 2/3 of
    the containing vectors size the map is reallocated to a vector of double the size. This is done to avoid
    excessive hash collisions.

    This structure corresponds most closely to the built in dict type and is intended as a replacement. Where the
    semantics are the same (more or less) the same function names have been used but for some cases it is not possible,
    for example assignments and deletion of values.

    PMap implements the Mapping protocol and is Hashable. It also supports dot-notation for
    element access.

    Random access and insert is log32(n) where n is the size of the map.

    The following are examples of some common operations on persistent maps

    >>> m1 = m(a=1, b=3)
    >>> m2 = m1.set('c', 3)
    >>> m3 = m2.remove('a')
    >>> m1
    pmap({'b': 3, 'a': 1})
    >>> m2
    pmap({'c': 3, 'b': 3, 'a': 1})
    >>> m3
    pmap({'c': 3, 'b': 3})
    >>> m3['c']
    3
    >>> m3.c
    3
    """
    __slots__ = ('_size', '_buckets', '__weakref__', '_cached_hash')

    def __new__(cls, size, buckets):
        self = super(PMap, cls).__new__(cls)
        self._size = size
        self._buckets = buckets
        return self

    @staticmethod
    def _get_bucket(buckets, key):
        index = hash(key) % len(buckets)
        bucket = buckets[index]
        return index, bucket

    @staticmethod
    def _getitem(buckets, key):
        _, bucket = PMap._get_bucket(buckets, key)
        if bucket:
            for k, v in bucket:
                if k == key:
                    return v

        raise KeyError(key)

    def __getitem__(self, key):
        return PMap._getitem(self._buckets, key)

    @staticmethod
    def _contains(buckets, key):
        _, bucket = PMap._get_bucket(buckets, key)
        if bucket:
            for k, _ in bucket:
                if k == key:
                    return True

            return False

        return False

    def __contains__(self, key):
        return self._contains(self._buckets, key)

    get = Mapping.get

    def __iter__(self):
        return self.iterkeys()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                "{0} has no attribute '{1}'".format(type(self).__name__, key)
            )

    def iterkeys(self):
        for k, _ in self.iteritems():
            yield k

    # These are more efficient implementations compared to the original
    # methods that are based on the keys iterator and then calls the
    # accessor functions to access the value for the corresponding key
    def itervalues(self):
        for _, v in self.iteritems():
            yield v

    def iteritems(self):
        for bucket in self._buckets:
            if bucket:
                for k, v in bucket:
                    yield k, v

    def values(self):
        return pvector(self.itervalues())

    def keys(self):
        return pvector(self.iterkeys())

    def items(self):
        return pvector(self.iteritems())

    def __len__(self):
        return self._size

    def __repr__(self):
        return 'pmap({0})'.format(str(dict(self)))

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Mapping):
            return NotImplemented
        if len(self) != len(other):
            return False
        if isinstance(other, PMap):
            if (hasattr(self, '_cached_hash') and hasattr(other, '_cached_hash')
                    and self._cached_hash != other._cached_hash):
                return False
            if self._buckets == other._buckets:
                return True
            return dict(self.iteritems()) == dict(other.iteritems())
        elif isinstance(other, dict):
            return dict(self.iteritems()) == other
        return dict(self.iteritems()) == dict(six.iteritems(other))

    __ne__ = Mapping.__ne__

    def __lt__(self, other):
        raise TypeError('PMaps are not orderable')

    __le__ = __lt__
    __gt__ = __lt__
    __ge__ = __lt__

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        if not hasattr(self, '_cached_hash'):
            self._cached_hash = hash(frozenset(self.iteritems()))
        return self._cached_hash

    def set(self, key, val):
        """
        Return a new PMap with key and val inserted.

        >>> m1 = m(a=1, b=2)
        >>> m2 = m1.set('a', 3)
        >>> m3 = m1.set('c' ,4)
        >>> m1
        pmap({'b': 2, 'a': 1})
        >>> m2
        pmap({'b': 2, 'a': 3})
        >>> m3
        pmap({'c': 4, 'b': 2, 'a': 1})
        """
        return self.evolver().set(key, val).persistent()

    def remove(self, key):
        """
        Return a new PMap without the element specified by key. Raises KeyError if the element
        is not present.

        >>> m1 = m(a=1, b=2)
        >>> m1.remove('a')
        pmap({'b': 2})
        """
        return self.evolver().remove(key).persistent()

    def discard(self, key):
        """
        Return a new PMap without the element specified by key. Returns reference to itself
        if element is not present.

        >>> m1 = m(a=1, b=2)
        >>> m1.discard('a')
        pmap({'b': 2})
        >>> m1 is m1.discard('c')
        True
        """
        try:
            return self.remove(key)
        except KeyError:
            return self

    def update(self, *maps):
        """
        Return a new PMap with the items in Mappings inserted. If the same key is present in multiple
        maps the rightmost (last) value is inserted.

        >>> m1 = m(a=1, b=2)
        >>> m1.update(m(a=2, c=3), {'a': 17, 'd': 35})
        pmap({'c': 3, 'b': 2, 'a': 17, 'd': 35})
        """
        return self.update_with(lambda l, r: r, *maps)

    def update_with(self, update_fn, *maps):
        """
        Return a new PMap with the items in Mappings maps inserted. If the same key is present in multiple
        maps the values will be merged using merge_fn going from left to right.

        >>> from operator import add
        >>> m1 = m(a=1, b=2)
        >>> m1.update_with(add, m(a=2))
        pmap({'b': 2, 'a': 3})

        The reverse behaviour of the regular merge. Keep the leftmost element instead of the rightmost.

        >>> m1 = m(a=1)
        >>> m1.update_with(lambda l, r: l, m(a=2), {'a':3})
        pmap({'a': 1})
        """
        evolver = self.evolver()
        for map in maps:
            for key, value in map.items():
                evolver.set(key, update_fn(evolver[key], value) if key in evolver else value)

        return evolver.persistent()

    def __add__(self, other):
        return self.update(other)

    def __reduce__(self):
        # Pickling support
        return pmap, (dict(self),)

    def transform(self, *transformations):
        """
        Transform arbitrarily complex combinations of PVectors and PMaps. A transformation
        consists of two parts. One match expression that specifies which elements to transform
        and one transformation function that performs the actual transformation.

        >>> from pyrsistent import freeze, ny
        >>> news_paper = freeze({'articles': [{'author': 'Sara', 'content': 'A short article'},
        ...                                   {'author': 'Steve', 'content': 'A slightly longer article'}],
        ...                      'weather': {'temperature': '11C', 'wind': '5m/s'}})
        >>> short_news = news_paper.transform(['articles', ny, 'content'], lambda c: c[:25] + '...' if len(c) > 25 else c)
        >>> very_short_news = news_paper.transform(['articles', ny, 'content'], lambda c: c[:15] + '...' if len(c) > 15 else c)
        >>> very_short_news.articles[0].content
        'A short article'
        >>> very_short_news.articles[1].content
        'A slightly long...'

        When nothing has been transformed the original data structure is kept

        >>> short_news is news_paper
        True
        >>> very_short_news is news_paper
        False
        >>> very_short_news.articles[0] is news_paper.articles[0]
        True
        """
        return transform(self, transformations)

    def copy(self):
        return self

    class _Evolver(object):
        __slots__ = ('_buckets_evolver', '_size', '_original_pmap')

        def __init__(self, original_pmap):
            self._original_pmap = original_pmap
            self._buckets_evolver = original_pmap._buckets.evolver()
            self._size = original_pmap._size

        def __getitem__(self, key):
            return PMap._getitem(self._buckets_evolver, key)

        def __setitem__(self, key, val):
            self.set(key, val)

        def set(self, key, val):
            if len(self._buckets_evolver) < 0.67 * self._size:
                self._reallocate(2 * len(self._buckets_evolver))

            kv = (key, val)
            index, bucket = PMap._get_bucket(self._buckets_evolver, key)
            if bucket:
                for k, v in bucket:
                    if k == key:
                        if v is not val:
                            new_bucket = [(k2, v2) if k2 != k else (k2, val) for k2, v2 in bucket]
                            self._buckets_evolver[index] = new_bucket

                        return self

                new_bucket = [kv]
                new_bucket.extend(bucket)
                self._buckets_evolver[index] = new_bucket
                self._size += 1
            else:
                self._buckets_evolver[index] = [kv]
                self._size += 1

            return self

        def _reallocate(self, new_size):
            new_list = new_size * [None]
            buckets = self._buckets_evolver.persistent()
            for k, v in chain.from_iterable(x for x in buckets if x):
                index = hash(k) % new_size
                if new_list[index]:
                    new_list[index].append((k, v))
                else:
                    new_list[index] = [(k, v)]

            # A reallocation should always result in a dirty buckets evolver to avoid
            # possible loss of elements when doing the reallocation.
            self._buckets_evolver = pvector().evolver()
            self._buckets_evolver.extend(new_list)

        def is_dirty(self):
            return self._buckets_evolver.is_dirty()

        def persistent(self):
            if self.is_dirty():
                self._original_pmap = PMap(self._size, self._buckets_evolver.persistent())

            return self._original_pmap

        def __len__(self):
            return self._size

        def __contains__(self, key):
            return PMap._contains(self._buckets_evolver, key)

        def __delitem__(self, key):
            self.remove(key)

        def remove(self, key):
            index, bucket = PMap._get_bucket(self._buckets_evolver, key)

            if bucket:
                new_bucket = [(k, v) for (k, v) in bucket if k != key]
                if len(bucket) > len(new_bucket):
                    self._buckets_evolver[index] = new_bucket if new_bucket else None
                    self._size -= 1
                    return self

            raise KeyError('{0}'.format(key))

    def evolver(self):
        """
        Create a new evolver for this pmap. For a discussion on evolvers in general see the
        documentation for the pvector evolver.

        Create the evolver and perform various mutating updates to it:

        >>> m1 = m(a=1, b=2)
        >>> e = m1.evolver()
        >>> e['c'] = 3
        >>> len(e)
        3
        >>> del e['a']

        The underlying pmap remains the same:

        >>> m1
        pmap({'b': 2, 'a': 1})

        The changes are kept in the evolver. An updated pmap can be created using the
        persistent() function on the evolver.

        >>> m2 = e.persistent()
        >>> m2
        pmap({'c': 3, 'b': 2})

        The new pmap will share data with the original pmap in the same way that would have
        been done if only using operations on the pmap.
        """
        return self._Evolver(self)

Mapping.register(PMap)
Hashable.register(PMap)


def _turbo_mapping(initial, pre_size):
    if pre_size:
        size = pre_size
    else:
        try:
            size = 2 * len(initial) or 8
        except Exception:
            # Guess we can't figure out the length. Give up on length hinting,
            # we can always reallocate later.
            size = 8

    buckets = size * [None]

    if not isinstance(initial, Mapping):
        # Make a dictionary of the initial data if it isn't already,
        # that will save us some job further down since we can assume no
        # key collisions
        initial = dict(initial)

    for k, v in six.iteritems(initial):
        h = hash(k)
        index = h % size
        bucket = buckets[index]

        if bucket:
            bucket.append((k, v))
        else:
            buckets[index] = [(k, v)]

    return PMap(len(initial), pvector().extend(buckets))


_EMPTY_PMAP = _turbo_mapping({}, 0)


def pmap(initial={}, pre_size=0):
    """
    Create new persistent map, inserts all elements in initial into the newly created map.
    The optional argument pre_size may be used to specify an initial size of the underlying bucket vector. This
    may have a positive performance impact in the cases where you know beforehand that a large number of elements
    will be inserted into the map eventually since it will reduce the number of reallocations required.

    >>> pmap({'a': 13, 'b': 14})
    pmap({'b': 14, 'a': 13})
    """
    if not initial:
        return _EMPTY_PMAP

    return _turbo_mapping(initial, pre_size)


def m(**kwargs):
    """
    Creates a new persitent map. Inserts all key value arguments into the newly created map.

    >>> m(a=13, b=14)
    pmap({'b': 14, 'a': 13})
    """
    return pmap(kwargs)
