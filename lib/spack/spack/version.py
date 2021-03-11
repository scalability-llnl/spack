# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module implements Version and version-ish objects.  These are:

Version
  A single version of a package.
VersionRange
  A range of versions of a package.
VersionList
  A list of Versions and VersionRanges.

All of these types support the following operations, which can
be called on any of the types::

  __eq__, __ne__, __lt__, __gt__, __ge__, __le__, __hash__
  __contains__
  satisfies
  overlaps
  union
  intersection
  concrete
"""
import re
from abc import ABCMeta, abstractmethod, abstractproperty
from bisect import bisect_left
from functools import wraps
from typing import Any, Callable, ClassVar, Dict, FrozenSet, Generic, Iterator, List, Optional, Tuple, Type, TypeVar, Union, cast  # novm
from typing import overload

from six import add_metaclass, string_types

from llnl.util.lang import memoized

import spack.error
from spack.util.spack_yaml import syaml_dict


__all__ = ['Version', 'VersionRange', 'VersionList', 'ver']

# Valid version characters
VALID_VERSION = re.compile(r'[A-Za-z0-9_\-]')

# regex for version segments
SEGMENT_REGEX = re.compile(r'[a-zA-Z]+|[0-9]+')

# Infinity-like versions. The order in the list implies the comparison rules
infinity_versions = ['develop', 'main', 'master', 'head', 'trunk']


def int_if_int(string):
    # type: (str) -> Union[str, int]
    """Convert a string to int if possible.  Otherwise, return a string."""
    try:
        return int(string)
    except ValueError:
        return string


def coerce_versions(a, b):
    # type: (Any, Any) -> Tuple[Any, Any]
    """
    Convert both a and b to the 'greatest' type between them, in this order:
           Version < VersionRange < VersionList
    This is used to simplify comparison operations below so that we're always
    comparing things that are of the same type.
    """
    order = (UnsignedVersion, WildcardVersion, Version, VersionRange, VersionList)
    ta, tb = type(a), type(b)

    def check_type(t):
        # type: (Type) -> None
        if t not in order:
            raise TypeError(
                "coerce_versions cannot be called on {0}: need one of {1}"
                .format(t, order))
    check_type(ta)
    check_type(tb)

    if ta == tb:
        return (a, b)
    if order.index(ta) < order.index(tb):
        if ta == UnsignedVersion:
            assert isinstance(a, WildcardVersion), a
            return (b, a)
        assert not isinstance(a, WildcardVersion), a
        if tb == VersionRange:
            assert isinstance(a, Version), a
            return (VersionRange.from_single_version(a), b)
        assert isinstance(a, (Version, VersionRange)), a
        assert isinstance(b, VersionList), b
        return (VersionList.from_version_or_range(a), b)

    def flipped(inp):
        # type: (Tuple[Any, Any]) -> Tuple[Any, Any]
        a, b = inp
        return b, a
    return flipped(coerce_versions(*flipped((a, b))))


def _coercing_factory(method, coerce_logic=False):
    @wraps(method)
    def coercing_method(a, b, *args, **kwargs):
        assert a is not None, a
        if coerce_logic and b is None:
            return False
        if type(a) == type(b) or b is None:
            return method(a, b, *args, **kwargs)
        ca, cb = coerce_versions(a, b)
        return getattr(ca, method.__name__)(cb, *args, **kwargs)
    return coercing_method


_T = TypeVar('_T', bound='Span')
_U = TypeVar('_U')


def coerced(
        method                       # type: Callable[[_T, _T], _U]
):
    # type: (...) -> Callable[[Span[_T], Span[_T]], _U]
    """Decorator that ensures that argument types of a method are coerced with
    `coerce_versions()`."""
    return cast('Callable[[Span[_T], Optional[Span[_T]]], _U]',
                _coercing_factory(method, coerce_logic=False))


def coerced_logic(
        method                                          # type: Callable[[_T, _U], bool]
):
    # type: (...) -> Callable[[_T, _U], bool]
    """Decorator that ensures that argument types of a method are coerced with
    `coerce_versions()`, and also returns False when the argument is None."""
    return cast('Callable[[Span[_T], Optional[_U]], bool]',
                _coercing_factory(method, coerce_logic=True))


def coerced_equals(
        method                                         # type: Callable[[_T, Any], bool]
):
    # type: (...) -> Callable[[Span[_T], Any], bool]
    """Decorator that ensures that argument types of a method are coerced with
    `coerce_versions()`, and also returns False when the argument is None."""
    return cast('Callable[[Span[_T], Any], bool]',
                _coercing_factory(method, coerce_logic=True))


@add_metaclass(ABCMeta)
class Span(Generic[_T]):
    """A class that spans some range of versions in some complicated way."""

    @abstractmethod
    def satisfies(self, other):
        # type: (_T) -> bool
        """Return whether any versions matched by this object match `other`."""

    @abstractmethod
    def overlaps(self, other):
        # type: (_T) -> bool
        """Return whether any versions matched by this object match `other`.

        In the case where a Version contains another Version (e.g. '1.1' contains '1'),
        .overlaps() will return False, while .satisfies() will return True.
        """

    @abstractmethod
    def __contains__(self, other):
        # type: (_T) -> bool
        """Return whether all versions matched by this object match `other`."""

    @abstractmethod
    def __eq__(self, other):
        # type: (Any) -> bool
        """Return whether `other` matches all the same versions."""

    @abstractmethod
    def __ne__(self, other):
        # type: (Any) -> bool
        pass

    @abstractmethod
    def __lt__(self, other):
        # type: (_T) -> bool
        """Return whether this contains a version lower than anything in `other`."""

    @abstractmethod
    def __le__(self, other):
        # type: (_T) -> bool
        pass

    @abstractmethod
    def __gt__(self, other):
        # type: (_T) -> bool
        """Return whether this contains a version greater than anything in `other`."""

    @abstractmethod
    def __ge__(self, other):
        # type: (_T) -> bool
        pass

    @abstractmethod
    def __hash__(self):
        # type: () -> int
        pass

    @abstractmethod
    def __str__(self):
        # type: () -> str
        """Return a string which returns the original object from .parse()."""

    def __format__(self, format_spec):
        # type: (str) -> str
        return str(self).format(format_spec)


class VersionPredicate(Span[_T]):
    """All top-level version-like objects will subclass this."""
    @classmethod
    @abstractmethod
    def parse(cls, string):
        # type: (str) -> _T
        """Parse a VersionPredicate object from a string."""

    def __repr__(self):
        # type: () -> str
        return '{0}.parse({1!r})'.format(
            type(self).__name__,
            str(self),
        )

    def copy(self):
        # type: () -> _T
        """Return a newly allocated object matching the same versions as this object."""

    @abstractmethod
    def lowest(self):
        # type: () -> Optional[Version]
        """Return the lowest version this object matches."""

    @abstractmethod
    def highest(self):
        # type: () -> Optional[Version]
        """Return the highest version this object matches."""

    @abstractproperty
    def concrete(self):
        # type: () -> Optional[Version]
        """If this points to exactly one Version, return it."""

    @abstractmethod
    def union(self, other):
        # type: (VersionPredicate) -> VersionPredicate
        """Return a VersionPredicate matching the union of two of this class."""

    @abstractmethod
    def intersection(self, other):
        # type: (VersionPredicate) -> VersionPredicate
        """Return a VersionPredicate matching the intersection of two of this class."""


@add_metaclass(ABCMeta)
class VersionInterface(Generic[_T]):
    @abstractmethod
    def is_predecessor(self, other):
        # type: (_T) -> bool
        """True if the other version is the immediate predecessor of this one.
           That is, NO versions v exist such that:
           (self < v < other and v not in self).
        """

    @abstractmethod
    def is_successor(self, other):
        # type: (_T) -> bool
        """Opposite of .is_predecessor()."""

    @abstractproperty
    def concrete_version(self):
        # type: () -> Optional[UnsignedVersion]
        pass

    @property
    def is_wildcard(self):
        # type: () -> bool
        return self.concrete_version is None


_V = TypeVar('_V', bound='VersionOperations')


@add_metaclass(ABCMeta)
class VersionOperations(Generic[_V]):
    @abstractproperty
    def dotted(self):
        # type: () -> _V
        """The dotted representation of the version.

        Example:
        >>> version = Version('1-2-3b')
        >>> version.dotted
        Version('1.2.3b')

        Returns:
            Version: The version with separator characters replaced by dots
        """

    @abstractproperty
    def underscored(self):
        # type: () -> _V
        """The underscored representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.underscored
        Version('1_2_3b')

        Returns:
            Version: The version with separator characters replaced by
                underscores
        """

    @abstractproperty
    def dashed(self):
        # type: () -> _V
        """The dashed representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.dashed
        Version('1-2-3b')

        Returns:
            Version: The version with separator characters replaced by dashes
        """

    @abstractproperty
    def joined(self):
        # type: () -> _V
        """The joined representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.joined
        Version('123b')

        Returns:
            Version: The version with separator characters removed
        """

    @abstractmethod
    def up_to(self, index):
        # type: (int) -> _V
        """The version up to the specified component.

        Examples:
        >>> version = Version('1.23-4b')
        >>> version.up_to(1)
        Version('1')
        >>> version.up_to(2)
        Version('1.23')
        >>> version.up_to(3)
        Version('1.23-4')
        >>> version.up_to(4)
        Version('1.23-4b')
        >>> version.up_to(-1)
        Version('1.23-4')
        >>> version.up_to(-2)
        Version('1.23')
        >>> version.up_to(-3)
        Version('1')

        Returns:
            Version: The first index components of the version
        """

    @abstractmethod
    def __len__(self):
        # type: () -> int
        """Return the number of components in this version."""

    @overload
    def __getitem__(self, idx):
        # type: (int) -> Union[str, int]
        pass

    @overload
    def __getitem__(self, idx):
        # type: (slice) -> _V
        pass

    @abstractmethod
    def __getitem__(self, idx):
        # type: (Union[int, slice]) -> Union[str, int, _V]
        """Return a prefix of this version."""

    @abstractmethod
    def isdevelop(self):
        # type: () -> bool
        """Triggers on the special case of the `@develop-like` version."""


class WildcardVersion(
        Span[VersionInterface],                             # type: ignore[type-var]
        VersionInterface[VersionInterface],                 # type: ignore[type-var]
):
    @property
    def concrete_version(self):
        # type: () -> Optional[UnsignedVersion]
        return None

    @coerced_logic
    def is_predecessor(self, other):                  # type: ignore[override]
        # type: (VersionInterface) -> bool
        return other.is_wildcard

    @coerced_logic
    def is_successor(self, other):                    # type: ignore[override]
        # type: (VersionInterface) -> bool
        return other.is_wildcard

    def satisfies(self, other):
        # type: (VersionInterface) -> bool
        return True

    def overlaps(self, other):
        # type: (VersionInterface) -> bool
        return True

    def __contains__(self, other):
        # type: (VersionInterface) -> bool
        return True

    def __eq__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, VersionInterface):
            return NotImplemented
        return other.is_wildcard

    def __ne__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, VersionInterface):
            return NotImplemented
        return not self == other

    def __lt__(self, other):
        # type: (VersionInterface) -> bool
        if self == other:
            return False
        return True

    def __le__(self, other):
        # type: (VersionInterface) -> bool
        return self == other or self < other

    def __gt__(self, other):
        # type: (VersionInterface) -> bool
        if self == other:
            return False
        return True

    def __ge__(self, other):
        # type: (VersionInterface) -> bool
        return self == other or self > other

    def __hash__(self):
        # type: () -> int
        return hash(str(self))

    def __str__(self):
        # type: () -> str
        return '*'


class UnsignedVersion(
        Span['UnsignedVersion'],
        VersionOperations['UnsignedVersion'],
        VersionInterface['UnsignedVersion'],
):
    """Class to represent versions"""

    _all_separators = frozenset(['.', '_', '-'])        # type: ClassVar[FrozenSet[str]]

    string = None                                    # type: str
    version = None                                   # type: Tuple[Union[str, int], ...]
    separators = None                                # type: Tuple[str, ...]

    def _coerced_separators(self, sep):
        # type: (str) -> str
        assert sep in type(self)._all_separators, (sep, type(self._all_separators))
        rest = type(self)._all_separators - set([sep])
        assert len(rest) == (len(type(self)._all_separators) - 1), rest
        string = self.string
        for s in rest:
            string = string.replace(s, sep)
        return string

    def _joined_separators(self):
        # type: () -> str
        string = self.string
        for sep in type(self)._all_separators:
            string = string.replace(sep, '')
        return string

    def __init__(self, string):
        # type: (Any) -> None
        if not isinstance(string, str):
            string = str(string)

        if not VALID_VERSION.match(string):
            raise ValueError("Bad characters in version string: %s" % string)

        # preserve the original string, but trimmed.
        string = string.strip()
        self.string = string

        # Split version into alphabetical and numeric segments
        segments = SEGMENT_REGEX.findall(string)
        self.version = tuple(int_if_int(seg) for seg in segments)

        # Store the separators from the original version string as well.
        self.separators = tuple(SEGMENT_REGEX.split(string)[1:])

    @memoized
    def _components(self):
        # type: () -> Tuple[Tuple[int, ...], Optional[str]]
        tag = None    # type: Optional[str]
        numbers = []  # type: List[int]
        for i, c in enumerate(self.version):
            if not isinstance(c, int):
                # If we have a string tag, we know it must be at the end.
                assert isinstance(c, str), c
                assert i == (len(self.version) - 1), (i, self.version)
                assert tag is None, tag
                tag = c
                continue
            numbers.append(c)
        return tuple(numbers), tag

    @property
    def version_components(self):
        # type: () -> Tuple[int, ...]
        numbers, _tag = self._components()
        return numbers

    @property
    def tag(self):
        # type: () -> Optional[str]
        _numbers, tag = self._components()
        return tag

    @property
    def concrete_version(self):
        # type: () -> Optional[UnsignedVersion]
        return self

    @property
    def dotted(self):
        # type: () -> UnsignedVersion
        """The dotted representation of the version.

        Example:
        >>> version = Version('1-2-3b')
        >>> version.dotted
        Version('1.2.3b')

        Returns:
            Version: The version with separator characters replaced by dots
        """
        return type(self)(self._coerced_separators('.'))

    @property
    def underscored(self):
        # type: () -> UnsignedVersion
        """The underscored representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.underscored
        Version('1_2_3b')

        Returns:
            Version: The version with separator characters replaced by
                underscores
        """
        return type(self)(self._coerced_separators('_'))

    @property
    def dashed(self):
        # type: () -> UnsignedVersion
        """The dashed representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.dashed
        Version('1-2-3b')

        Returns:
            Version: The version with separator characters replaced by dashes
        """
        return type(self)(self._coerced_separators('-'))

    @property
    def joined(self):
        # type: () -> UnsignedVersion
        """The joined representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.joined
        Version('123b')

        Returns:
            Version: The version with separator characters removed
        """
        return type(self)(self._joined_separators())

    def up_to(self, index):
        # type: (int) -> UnsignedVersion
        """The version up to the specified component.

        Examples:
        >>> version = Version('1.23-4b')
        >>> version.up_to(1)
        Version('1')
        >>> version.up_to(2)
        Version('1.23')
        >>> version.up_to(3)
        Version('1.23-4')
        >>> version.up_to(4)
        Version('1.23-4b')
        >>> version.up_to(-1)
        Version('1.23-4')
        >>> version.up_to(-2)
        Version('1.23')
        >>> version.up_to(-3)
        Version('1')

        Returns:
            Version: The first index components of the version
        """
        return cast(UnsignedVersion, self[:index])

    def __iter__(self):
        # type: () -> Iterator[Union[str, int]]
        # NB: This does not override anything!
        return iter(self.version)

    def __len__(self):
        # type: () -> int
        return len(self.version)

    @overload
    def __getitem__(self, idx):
        # type: (int) -> Union[str, int]
        pass

    @overload
    def __getitem__(self, idx):
        # type: (slice) -> UnsignedVersion
        pass

    def __getitem__(self, idx):
        # type: (Union[int, slice]) -> Union[str, int, UnsignedVersion]
        cls = type(self)

        if isinstance(idx, int):
            return self.version[idx]

        elif isinstance(idx, slice):
            string_arg = []  # type: List[str]

            pairs = zip(self.version[idx], self.separators[idx])
            for token, sep in pairs:
                string_arg.append(str(token))
                string_arg.append(str(sep))

            string_arg.pop()  # We don't need the last separator
            return cls(''.join(string_arg))

        message = '{cls.__name__} indices must be integers'
        raise TypeError(message.format(cls=cls))

    def isdevelop(self):
        # type: () -> bool
        """Triggers on the special case of the `@develop-like` version."""
        for inf in infinity_versions:
            for v in self.version:
                if v == inf:
                    return True
        return False

    @coerced_logic
    def is_predecessor(self, other):
        # type: (UnsignedVersion) -> bool
        """True if the other version is the immediate predecessor of this one.
           That is, NO versions v exist such that:
           (self < v < other and v not in self).
        """
        if len(self.version_components) > len(other.version_components):
            # 1.0 !<| 1
            return False
        if len(self.version_components) < len(other.version_components):
            shared_prefix = other.version_components[:len(self.version_components)]
            if self.version_components != shared_prefix:
                # 1 !<| 2.0
                return False
            unshared_suffix = other.version_components[len(self.version_components):]
            assert bool(unshared_suffix), unshared_suffix
            # 1 <| 1.0
            return all(x == 0 for x in unshared_suffix)
        assert len(self.version_components) == len(other.version_components)
        # 1.1 <| 1.2
        assert len(self.version_components) > 0, self
        sl = self.version_components[-1]
        ol = other.version_components[-1]
        return (ol - sl) == 1

    @coerced_logic
    def is_successor(self, other):
        # type: (UnsignedVersion) -> bool
        return other.is_predecessor(self)

    @coerced_logic
    def satisfies(self, other):
        # type: (UnsignedVersion) -> bool
        # return self in other
        raise NotImplementedError(self)

    @coerced_logic
    def overlaps(self, other):
        # type: (UnsignedVersion) -> bool
        # return self in other or other in self
        raise NotImplementedError(self)

    @coerced_logic
    def __contains__(self, other):
        # type: (UnsignedVersion) -> bool
        return other.version[:len(self.version)] == self.version

    # TODO: consider @memoized since we impl __hash__?
    @coerced_logic
    def __lt__(self, other):                           # type: ignore[has-type]
        # type: (UnsignedVersion) -> bool
        """Version comparison is designed for consistency with the way RPM
           does things.  If you need more complicated versions in installed
           packages, you should override your package's version string to
           express it more sensibly.
        """
        # Coerce if other is not a Version
        # simple equality test first.
        if self.version == other.version:
            return False

        # Standard comparison of two numeric versions
        for a, b in zip(self.version, other.version):
            if a == b:
                continue
            else:
                if a in infinity_versions:
                    if b in infinity_versions:
                        return (infinity_versions.index(a) >  # type: ignore[arg-type]
                                infinity_versions.index(b))   # type: ignore[arg-type]
                    else:
                        return False
                if b in infinity_versions:
                    return True

                # Neither a nor b is infinity
                # Numbers are always "newer" than letters.
                # This is for consistency with RPM.  See patch
                # #60884 (and details) from bugzilla #50977 in
                # the RPM project at rpm.org.  Or look at
                # rpmvercmp.c if you want to see how this is
                # implemented there.
                if type(a) != type(b):
                    return type(b) == int
                else:
                    return a < b                            # type: ignore[operator]

        # If the common prefix is equal, the one
        # with more segments is bigger.
        return len(self.version) < len(other.version)

    @coerced_equals
    def __eq__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, UnsignedVersion):
            return NotImplemented
        return self.version == other.version

    @coerced_equals
    def __ne__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, UnsignedVersion):
            return NotImplemented
        return not (self == other)

    @coerced_logic
    def __le__(self, other):                           # type: ignore[has-type]
        # type: (UnsignedVersion) -> bool
        return self == other or self < other

    @coerced_logic
    def __ge__(self, other):
        # type: (UnsignedVersion) -> bool
        return not (self < other)

    @coerced_logic
    def __gt__(self, other):
        # type: (UnsignedVersion) -> bool
        return not (self == other) and not (self < other)

    def __hash__(self):
        # type: () -> int
        return hash(self.version)

    def __str__(self):
        # type: () -> str
        return self.string


class Version(
        VersionPredicate['Version'],
        VersionOperations['Version'],
        VersionInterface['Version'],
):
    _unsigned_version = None  # type: Union[WildcardVersion, UnsignedVersion]
    _negate = None            # type: bool

    @classmethod
    def parse(cls, string):
        # type: (str) -> Version
        if string.startswith('!'):
            string = string[1:]
            negate = True
        else:
            negate = False
        inner = (WildcardVersion() if string == '*'
                 else UnsignedVersion(string)
                 )  # type: Union[WildcardVersion, UnsignedVersion]
        return cls(inner, negate=negate)

    @classmethod
    def wildcard(cls):
        # type: () -> Version
        return cls(unsigned_version=WildcardVersion(), negate=False)

    def __init__(self, unsigned_version, negate=False):
        # type: (Union[str, WildcardVersion, UnsignedVersion], bool) -> None
        if isinstance(unsigned_version, str):
            unsigned_version = UnsignedVersion(unsigned_version)
        self._unsigned_version = unsigned_version
        self._negate = negate

    @property
    def polarity(self):
        # type: () -> bool
        return not self._negate

    @property
    def unsigned_form(self):
        # type: () -> Union[WildcardVersion, UnsignedVersion]
        return self._unsigned_version

    @property
    def string(self):
        # type: () -> str
        return str(self.unsigned_form)

    def _wildcard_defaulted(self, default, fun):
        # type: (_U, Callable[[UnsignedVersion], _U]) -> _U
        if self.is_wildcard:
            return default
        assert isinstance(self.unsigned_form, UnsignedVersion), self
        return fun(self.unsigned_form)

    @property
    def version(self):
        # type: () -> Tuple[Union[str, int], ...]
        return self._wildcard_defaulted((), lambda u: u.version)

    @property
    def separators(self):
        # type: () -> Tuple[str, ...]
        return self._wildcard_defaulted((), lambda u: u.separators)

    @property
    def concrete_version(self):
        # type: () -> Optional[UnsignedVersion]
        return self.unsigned_form.concrete_version

    def lowest(self):
        # type: () -> Optional[Version]
        if self.is_wildcard:
            return None
        return self

    def highest(self):
        # type: () -> Optional[Version]
        if self.is_wildcard:
            return None
        return self

    @property
    def concrete(self):
        # type: () -> Optional[Version]
        if self.is_wildcard:
            return None
        return self

    def _copy(self, unsigned_version):
        # type: (Union[UnsignedVersion, WildcardVersion]) -> Version
        return type(self)(unsigned_version=unsigned_version,
                          negate=self._negate)

    def copy(self):
        # type: () -> Version
        return self._copy(self.unsigned_form)

    @property
    def dotted(self):
        # type: () -> Version
        return self._wildcard_defaulted(self, lambda u: self._copy(u.dotted))

    @property
    def underscored(self):
        # type: () -> Version
        return self._wildcard_defaulted(self, lambda u: self._copy(u.underscored))

    @property
    def dashed(self):
        # type: () -> Version
        return self._wildcard_defaulted(self, lambda u: self._copy(u.dashed))

    @property
    def joined(self):
        # type: () -> Version
        return self._wildcard_defaulted(self, lambda u: self._copy(u.joined))

    def up_to(self, index):
        # type: (int) -> Version
        return self._wildcard_defaulted(self, lambda u: self._copy(u.up_to(index)))

    def __len__(self):
        # type: () -> int
        return self._wildcard_defaulted(0, len)

    @overload
    def __getitem__(self, idx):
        # type: (int) -> Union[str, int]
        pass

    @overload
    def __getitem__(self, idx):
        # type: (slice) -> Version
        pass

    def __getitem__(self, idx):
        # type: (Union[int, slice]) -> Union[str, int, Version]
        if self.is_wildcard:
            if isinstance(idx, int):
                raise TypeError(
                    'cannot fetch individual index {0} from wildcard version: {1}'
                    .format(idx, self))
            return self
        assert isinstance(self.unsigned_form, UnsignedVersion), self
        if isinstance(idx, int):
            return self.unsigned_form[idx]
        new_unsigned = self.unsigned_form[idx]
        assert isinstance(new_unsigned, UnsignedVersion), new_unsigned
        return self._copy(new_unsigned)

    def isdevelop(self):
        # type: () -> bool
        return self._wildcard_defaulted(False, lambda u: u.isdevelop())

    @coerced_logic
    def is_predecessor(self, other):
        # type: (Version) -> bool
        return (
            # 1 <| 1.0
            (self.polarity and other.polarity and
             self.unsigned_form.is_predecessor(other.unsigned_form)) or
            # !1.0 !<| !1
            # !1.0 <| 1
            # !1.0 <| 1.0
            # !1 <| 1.0
            (other.polarity and not self.polarity and
             (self.unsigned_form == other.unsigned_form or
              self.unsigned_form.is_predecessor(other.unsigned_form) or
              self.unsigned_form.is_successor(other.unsigned_form))
             ) or
            # 1.0 <| !1.0
            # 1.0 !<| !1
            # 1 !<| !1.0
            (self.polarity and not other.polarity and
             self.unsigned_form == other.unsigned_form)
        )

    @coerced_logic
    def is_successor(self, other):
        # type: (Version) -> bool
        return other.is_predecessor(self)

    @coerced_logic
    def satisfies(self, other):
        # type: (Version) -> bool
        """A Version 'satisfies' another if it is at least as specific and has
        a common prefix.  e.g., we want gcc@4.7.3 to satisfy a request for
        gcc@4.7 so that when a user asks to build with gcc@4.7, we can find
        a suitable compiler.
        """
        return self in other

    @coerced_logic
    def overlaps(self, other):
        # type: (Version) -> bool
        return self in other or other in self
        # return (not self < other) or (not self > other)

    @coerced_logic
    def __contains__(self, other):
        # type: (Version) -> bool
        # return not (other < self or other > self)
        return (
            # 1 \in 1
            # 1.0 \in 1
            (self.polarity and other.polarity and
             other.unsigned_form in self.unsigned_form) or
            # !1 \in !1.0
            # !1 \in !1
            (not self.polarity and not other.polarity and
             self.unsigned_form in other.unsigned_form) or
            # +* \in !* (unless * == *)
            (not self.polarity and other.polarity)
        )

    @coerced_logic
    def __lt__(self, other):                                # type: ignore[has-type]
        # type: (Version) -> bool
        return (
            # 2 < 3
            # 1 !< 1.0 (successor)
            # 1 < 1.1
            # !2 !< !3
            (self.polarity and
             other.polarity and
             self.unsigned_form < other.unsigned_form) or
            # !* < +*
            (other.polarity and not self.polarity and
             (self.unsigned_form == other.unsigned_form or
              self.unsigned_form < other.unsigned_form or
              self.unsigned_form > other.unsigned_form)
             ) or
            # ???
            (self.polarity and not other.polarity and
             self.unsigned_form == other.unsigned_form)
        )

    @coerced_logic
    def __gt__(self, other):
        # type: (Version) -> bool
        return (
            # 3 > 2
            # 1.0 !> 1 (successor)
            # 1.1 > 1
            # !3 !> !2
            (self.polarity and
             other.polarity and
             self.unsigned_form > other.unsigned_form) or
            # !* < +*
            (other.polarity and not self.polarity and
             (self.unsigned_form == other.unsigned_form or
              self.unsigned_form < other.unsigned_form or
              self.unsigned_form > other.unsigned_form)
             ) or
            # ???
            (self.polarity and not other.polarity and
             self.unsigned_form == other.unsigned_form)
        )

    @coerced_equals
    def __eq__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, Version):
            return NotImplemented
        return (self.unsigned_form == other.unsigned_form and
                self.polarity == other.polarity)

    @coerced_equals
    def __ne__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, Version):
            return NotImplemented
        return not self == other

    @coerced_logic
    def __le__(self, other):                                # type: ignore[has-type]
        # type: (Version) -> bool
        return self == other or self < other

    @coerced_logic
    def __ge__(self, other):
        # type: (Version) -> bool
        return self == other or self > other

    def __hash__(self):
        # type: () -> int
        return hash((self.unsigned_form, self.polarity))

    def __str__(self):
        # type: () -> str
        negated_mark = '!' if self._negate else ''
        return '{0}{1}'.format(negated_mark, self.unsigned_form)

    def negated(self):
        # type: () -> Version
        return type(self)(unsigned_version=self.unsigned_form,
                          negate=not self._negate)

    @coerced
    def union(self, other):
        # type: (Version) -> VersionPredicate
        if self == other or other in self:
            return self
        if self in other:
            return other
        return VersionList([self, other])

    @coerced
    def intersection(self, other):
        # type: (Version) -> VersionPredicate
        if self == other:
            return self
        return VersionList.empty()


def _endpoint_only(fun):
    # type: (Callable[[_VersionEndpoint, _VersionEndpoint], bool]) -> Callable[[_VersionEndpoint, _VersionEndpoint], bool]
    """We want to avoid logic that handles any type of version range, just endpoints."""
    @wraps(fun)
    def validate_endpoint_argument(self, other):
        # type: (_VersionEndpoint, _VersionEndpoint) -> bool
        assert isinstance(other, _VersionEndpoint), (
            "required two _VersionEndpoint arguments, received {0} and {1}"
            .format(self, other))
        return fun(self, other)
    return validate_endpoint_argument


class _VersionEndpoint(Span['_VersionEndpoint']):
    value = None                                            # type: Version
    location = None                                         # type: str

    _valid_endpoint_locations = frozenset([
        'left', 'right',
    ])                                                  # type: ClassVar[FrozenSet[str]]

    def __init__(self, value, location):
        # type: (Version, str, bool) -> None
        assert isinstance(value, Version), value
        assert location in self._valid_endpoint_locations, location

        self.value = value
        self.location = location

    def __repr__(self):
        # type: () -> str
        return ("_VersionEndpoint(value={0!r}, location={1!r})"
                .format(self.value, self.location))

    def __str__(self):
        # type: () -> str
        raise NotImplementedError(self)

    def overlaps(self, other):
        # type: (_VersionEndpoint) -> bool
        raise NotImplementedError(self)

    def satisfies(self, other):
        # type: (_VersionEndpoint) -> bool
        raise NotImplementedError(self)

    def __hash__(self):
        # type: () -> int
        return hash((self.value, self.location))

    def __contains__(self, other):
        # type: (_VersionEndpoint) -> bool
        # raise NotImplementedError(self)
        # return not (other < self or other > self)
        if self.location == 'right':
            return (other.value < self.value or
                    other.value in self.value)
        assert self.location == 'left', self
        return (other.value > self.value or
                other.value in self.value)

    def lowest(self):
        # type: () -> Optional[Version]
        if self.location == 'left':
            return self.value.lowest()
        return None

    def highest(self):
        # type: () -> Optional[Version]
        if self.location == 'right':
            return self.value.highest()
        return None

    def __eq__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, _VersionEndpoint):
            return NotImplemented
        return (self.value == other.value and self.location == other.location)

    # TODO: consider @memoized since we impl __hash__?
    @_endpoint_only
    def __lt__(self, other):
        # type: (_VersionEndpoint) -> bool
        assert not (
            self.location == 'right' or other.location == 'right'), (self, other)
        return self.value < other.value

    @_endpoint_only
    def __gt__(self, other):
        # type: (_VersionEndpoint) -> bool
        assert not (
            self.location == 'left' or other.location == 'left'), (self, other)
        return self.value > other.value

    def __ne__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, _VersionEndpoint):
            return NotImplemented
        return not (self == other)

    @_endpoint_only
    def __le__(self, other):
        # type: (_VersionEndpoint) -> bool
        return self == other or self < other

    @_endpoint_only
    def __ge__(self, other):
        # type: (_VersionEndpoint) -> bool
        return self == other or self < other


class _EndpointContainment(object):
    low_contained = None          # type: bool
    high_contained = None         # type: bool

    def __init__(
            self,
            self_low,                                       # type: _VersionEndpoint
            self_high,                                      # type: _VersionEndpoint
            other_low,                                      # type: _VersionEndpoint
            other_high,                                     # type: _VersionEndpoint
    ):
        # type: (...) -> None
        assert isinstance(self_low, _VersionEndpoint) and self_low.location == 'left'
        assert isinstance(self_high, _VersionEndpoint) and self_high.location == 'right'
        assert isinstance(other_low, _VersionEndpoint) and other_low.location == 'left'
        assert (isinstance(other_high, _VersionEndpoint) and
                other_high.location == 'right')
        self.low_contained = ((other_low in self_low) and (other_low in self_high))
        self.high_contained = ((other_high in self_low) and (other_high in self_low))
        # import pdb; pdb.set_trace()


class VersionRange(VersionPredicate['VersionRange']):
    start = None                    # type: Version
    end = None                      # type: Version

    @classmethod
    def from_single_version(cls, version):
        # type: (Version) -> VersionRange
        return cls(start=version, end=version)

    @classmethod
    def parse(cls, string):
        # type: (str) -> VersionRange
        if string.startswith(':'):
            if string.startswith(':!'):
                if string.endswith('!:'):
                    # :!<x>!:
                    version = Version.parse(string[2:-2])
                    return VersionRange.from_single_version(version.negated())
                assert not string.endswith(':'), string
                # :!<x>
                version = Version.parse(string[2:])
                return VersionRange(start=Version.wildcard(), end=version.negated())
            if string.endswith(':'):
                # :
                # We ban :!<x>: and :<x>:.
                assert string == ':', string
                return VersionRange(start=Version.wildcard(), end=Version.wildcard())
            # :<x>
            version = Version.parse(string[1:])
            return VersionRange(start=Version.wildcard(), end=version)
        if string.endswith(':'):
            if string.endswith('!:'):
                # <x>!:
                version = Version.parse(string[:-2])
                return VersionRange(start=version.negated(), end=Version.wildcard())
            # <x>:
            version = Version.parse(string[:-1])
            return VersionRange(start=version, end=Version.wildcard())
        if ':' in string:
            # <x>:<x> | <x>!:<x> | <x>:!<x> | <x>!:!<x>
            start, end = tuple(string.split(':'))
            return VersionRange(start=Version.parse(start), end=Version.parse(end))
        # <x>
        version = Version.parse(string)
        return VersionRange.from_single_version(version)

    def __init__(
            self,
            start,                                 # type: Optional[Union[str, Version]]
            end,                                   # type: Optional[Union[str, Version]]
    ):
        if isinstance(start, string_types):
            start = Version.parse(start)
        elif start is None:
            start = Version.wildcard()
        assert isinstance(start, Version), start

        if isinstance(end, string_types):
            end = Version.parse(end)
        elif end is None:
            end = Version.wildcard()
        assert isinstance(end, Version), end

        self.start = start
        self.end = end

        if start.polarity and end.polarity and end < start:
            raise ValueError("Invalid Version range: {0}: end must be before start"
                             .format(self))

    def lowest(self):
        # type: () -> Optional[Version]
        return self._low_endpoint().lowest()

    @memoized
    def _low_endpoint(self):
        # type: () -> _VersionEndpoint
        return _VersionEndpoint(self.start, 'left')

    def highest(self):
        # type: () -> Optional[Version]
        return self._high_endpoint().highest()

    @memoized
    def _high_endpoint(self):
        # type: () -> _VersionEndpoint
        return _VersionEndpoint(self.end, 'right')

    @memoized
    def _endpoint_containment(self, other):
        # type: (VersionRange) -> _EndpointContainment
        return _EndpointContainment(
            self_low=self._low_endpoint(),
            self_high=self._high_endpoint(),
            other_low=other._low_endpoint(),
            other_high=other._high_endpoint(),
        )

    @coerced_logic
    def __lt__(self, other):                              # type: ignore[has-type]
        # type: (VersionRange) -> bool
        """Sort VersionRanges lexicographically so that they are ordered first
           by start and then by end.  None denotes an open range, so None in
           the start position is less than everything except None, and None in
           the end position is greater than everything but None.
        """
        return self._low_endpoint() < other._low_endpoint()

    @coerced_logic
    def __gt__(self, other):
        # type: (VersionRange) -> bool
        return self._high_endpoint() > other._high_endpoint()

    @coerced_equals
    def __eq__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, VersionRange):
            return NotImplemented
        return (self.start == other.start and self.end == other.end)

    @coerced_equals
    def __ne__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, VersionRange):
            return NotImplemented
        return not (self == other)

    @coerced_logic
    def __le__(self, other):                              # type: ignore[has-type]
        # type: (VersionRange) -> bool
        return self == other or self < other

    @coerced_logic
    def __ge__(self, other):
        # type: (VersionRange) -> bool
        return self == other or self > other

    def _is_single_version(self):
        # type: () -> bool
        return (self.start.polarity and self.end.polarity and
                self.start == self.end and
                not self.start.is_wildcard and
                not self.end.is_wildcard)

    @property
    def concrete(self):
        # type: () -> Optional[Version]
        if self._is_single_version():
            return self.start
        return None

    @coerced_logic
    def __contains__(self, other):
        # type: (VersionRange) -> bool
        containment = self._endpoint_containment(other)
        return containment.low_contained and containment.high_contained

    @coerced_logic
    def satisfies(self, other):
        # type: (VersionRange) -> bool
        """A VersionRange satisfies another if some version in this range
        would satisfy some version in the other range.  To do this it must
        either:

        a) Overlap with the other range
        b) The start of this range satisfies the end of the other range.

        This is essentially the same as overlaps(), but overlaps assumes
        that its arguments are specific.  That is, 4.7 is interpreted as
        4.7.0.0.0.0... .  This function assumes that 4.7 would be satisfied
        by 4.7.3.5, etc.

        Rationale:

        If a user asks for gcc@4.5:4.7, and a package is only compatible with
        gcc@4.7.3:4.8, then that package should be able to build under the
        constraints.  Just using overlaps() would not work here.

        Note that we don't need to check whether the end of this range
        would satisfy the start of the other range, because overlaps()
        already covers that case.

        Note further that overlaps() is a symmetric operation, while
        satisfies() is not.
        """
        return self in other

    @coerced_logic
    def overlaps(self, other):
        # type: (VersionRange) -> bool
        containment = self._endpoint_containment(other)
        return containment.low_contained or containment.high_contained

    @coerced
    def union(self, other):
        # type: (VersionRange) -> VersionPredicate
        if not self.overlaps(other):
            if self.end.is_predecessor(other.start):
                return VersionRange(self.start, other.end)

            if other.end.is_predecessor(self.start):
                return VersionRange(other.start, self.end)

            return VersionList([self, other])

        # if we're here, then we know the ranges overlap.
        if self.start.is_wildcard or other.start.is_wildcard:
            start = Version.wildcard()
        else:
            start = self.start

        # TODO: See note in intersection() about < and in discrepancy.
        if self.start in other.start or other.start < self.start:
            start = other.start

        if self.end.is_wildcard or other.end.is_wildcard:
            end = Version.wildcard()
        else:
            end = self.end

        # TODO: See note in intersection() about < and in discrepancy.
        if other.end not in self.end:
            if end in other.end or other.end > self.end:
                end = other.end

        return VersionRange(start, end)

    @coerced
    def intersection(self, other):
        # type: (VersionRange) -> VersionPredicate
        if self.overlaps(other):
            if self.start.is_wildcard:
                start = other.start
            else:
                start = self.start

            if other.start > start or other.start in start:
                start = other.start

            if self.end.is_wildcard:
                end = other.end
            else:
                end = self.end

            # TODO: does this make sense?
            # This is tricky:
            #     1.6.5 in 1.6 = True  (1.6.5 is more specific)
            #     1.6 < 1.6.5  = True  (lexicographic)
            # Should 1.6 NOT be less than 1.6.5?  Hmm.
            # Here we test (not end in other.end) first to avoid paradox.
            # FIXME: this seems to make perfect sense? Has this code ever
            # stopped any error?
            if end not in other.end:
                if other.end < end or other.end in end:
                    end = other.end

            return VersionRange(start, end)
        return VersionList.empty()

    def __hash__(self):
        return hash((self.start, self.end))

    def __str__(self):
        # ( :!<x>!: | <x> | : )
        if self.start == self.end:
            if self.start.is_wildcard or self.end.is_wildcard:
                assert self.start.is_wildcard and self.end.is_wildcard, self.end
                if self.start.polarity:
                    # :
                    return ':'
                assert not self.end.polarity, self.end
                # :!<x>!:
                return ":!{0}!:".format(self.start.unsigned_form)
            # <x>
            return str(self.start.unsigned_form)
        # ( :!<x> | :<x> )
        if self.start.is_wildcard:
            # Checked that self.start == self.end above.
            assert not self.end.is_wildcard, self.end
            assert self.start.polarity, self
            # :<x>
            if self.end.polarity:
                return ':{0}'.format(self.end.unsigned_form)
            # :!<x>
            return ':!{0}'.format(self.end.unsigned_form)
        # ( <x>: | <x>!: )
        if self.end.is_wildcard:
            assert not self.start.is_wildcard, self.start
            assert self.end.polarity, self
            # <x>:
            if self.start.polarity:
                return '{0}:'.format(self.start.unsigned_form)
            # <x>!:
            return '{0}!:'.format(self.start.unsigned_form)
        # {0}!:!{1} => {0} < x < {1}
        if (not self.start.polarity and
            not self.end.polarity):
            return '{0}!:!{1}'.format(self.start.unsigned_form, self.end.unsigned_form)
        # {0}:!{1} => {0} <= x < {1}
        if not self.end.polarity:
            return '{0}:!{1}'.format(self.start.unsigned_form, self.end.unsigned_form)
        # {0}!:{1} => {0} < x <= {1}
        if not self.start.polarity:
            return '{0}!:{1}'.format(self.start.unsigned_form, self.end.unsigned_form)
        # {0}:{1} => {0} <= x <= {1}
        assert self.start.polarity and self.end.polarity
        return "{0}:{1}".format(self.start.unsigned_form, self.end.unsigned_form)


class VersionList(VersionPredicate['VersionList']):
    """Sorted, non-redundant list of Versions and VersionRanges."""
    versions = None  # type: List[Union[Version, VersionRange]]

    @classmethod
    def from_version_or_range(cls, version_or_range):
        # type: (Union[Version, VersionRange]) -> VersionList
        return cls([version_or_range])

    @classmethod
    def empty(cls):
        # type: () -> VersionList
        return cls(vlist=None)

    @classmethod
    def parse(cls, string):
        # type: (str) -> VersionList

        def parse_version_or_range(el):
            # type: (str) -> Union[Version, VersionRange]
            if ':' in el:
                return VersionRange.parse(el)
            return Version.parse(el)
        if ',' in string:
            elements = string.split(',')
            versions_or_ranges = [parse_version_or_range(el) for el in elements]
            return cls(versions_or_ranges)
        if string:
            return cls([parse_version_or_range(string)])
        return cls.empty()

    def __init__(self, vlist=None):
        # type: (Optional[Union[VersionList, str, Version, VersionRange, List[Union[Version, VersionRange]]]]) -> None
        self.versions = []  # type: List[Union[Version, VersionRange]]
        if vlist is not None:
            if isinstance(vlist, string_types):
                vv = _string_to_version(
                    vlist)             # type: Union[Version, VersionRange, VersionList]
                if isinstance(vv, VersionList):
                    self.versions = vv.versions
                else:
                    self.versions = [vv]
            else:
                vs = list(vlist)                            # type: ignore[arg-type]
                for v in vs:
                    self.add(ver(v))

    def add(self, version):
        if type(version) in (Version, VersionRange):
            # This normalizes single-value version ranges.
            if version.concrete:
                version = version.concrete

            i = bisect_left(self, version)

            while i - 1 >= 0 and version.overlaps(self[i - 1]):
                version = version.union(self[i - 1])
                del self.versions[i - 1]
                i -= 1

            while i < len(self) and version.overlaps(self[i]):
                version = version.union(self[i])
                del self.versions[i]

            self.versions.insert(i, version)

        elif type(version) == VersionList:
            for v in version:
                self.add(v)

        else:
            raise TypeError("Can't add %s to VersionList" % type(version))

    @property
    def concrete(self):
        # type: () -> Optional[Version]
        if len(self) == 1:
            return self[0].concrete
        else:
            return None

    def copy(self):
        # type: () -> VersionList
        return VersionList(self)

    def lowest(self):
        # type: () -> Optional[Version]
        """Get the lowest version in the list."""
        if not self:
            return None
        else:
            return self[0].lowest()

    def highest(self):
        # type: () -> Optional[Version]
        """Get the highest version in the list."""
        if not self:
            return None
        else:
            return self[-1].highest()

    def highest_numeric(self):
        # type: () -> Optional[Version]
        """Get the highest numeric version in the list."""
        numeric_versions = list(filter(
            lambda v: str(v) not in infinity_versions,
            self.versions))
        if not any(numeric_versions):
            return None
        else:
            return numeric_versions[-1].highest()

    def preferred(self):
        # type: () -> Optional[Version]
        """Get the preferred (latest) version in the list."""
        latest = self.highest_numeric()
        if latest is None:
            latest = self.highest()
        return latest

    @coerced_logic
    def overlaps(self, other):
        # type: (VersionList) -> bool
        if not other or not self:
            return False

        s = o = 0
        while s < len(self) and o < len(other):
            if self[s].overlaps(other[o]):
                return True
            elif self[s] < other[o]:
                s += 1
            else:
                o += 1
        return False

    def to_dict(self):
        # type: () -> Dict[str, Union[str, List[str]]]
        """Generate human-readable dict for YAML."""
        if self.concrete:
            return syaml_dict([
                ('version', str(self[0]))
            ])
        else:
            return syaml_dict([
                ('versions', [str(v) for v in self])
            ])

    @staticmethod
    def from_dict(dictionary):
        # type: (Dict[str, Union[str, List[str]]]) -> VersionList
        """Parse dict from to_dict."""
        if 'versions' in dictionary:
            return VersionList(dictionary['versions'])      # type: ignore[arg-type]
        elif 'version' in dictionary:
            return VersionList([dictionary['version']])     # type: ignore[list-item]
        else:
            raise ValueError("Dict must have 'version' or 'versions' in it.")

    @coerced_logic
    def satisfies(self, other, strict=False):
        # type: (VersionList, bool) -> bool
        """A VersionList satisfies another if some version in the list
           would satisfy some version in the other list.  This uses
           essentially the same algorithm as overlaps() does for
           VersionList, but it calls satisfies() on member Versions
           and VersionRanges.

           If strict is specified, this version list must lie entirely
           *within* the other in order to satisfy it.
        """
        if not other or not self:
            return False

        if strict:
            return self in other

        s = o = 0
        while s < len(self) and o < len(other):
            if self[s].satisfies(other[o]):
                return True
            elif self[s] < other[o]:
                s += 1
            else:
                o += 1
        return False

    @coerced
    def update(self, other):
        # type: (VersionList) -> None
        for v in other.versions:
            self.add(v)

    @coerced
    def union(self, other):
        # type: (VersionList) -> VersionList
        result = self.copy()
        result.update(other)
        return result

    @coerced
    def intersection(self, other):
        # type: (VersionList) -> VersionList
        # TODO: make this faster.  This is O(n^2).
        result = VersionList()
        for s in self:
            for o in other:
                result.add(s.intersection(o))               # type: ignore[arg-type]
        return result

    @coerced
    def intersect(self, other):
        # type: (VersionList) -> bool
        """Intersect this spec's list with other.

        Return True if the spec changed as a result; False otherwise
        """
        isection = self.intersection(other)
        changed = (isection.versions != self.versions)
        self.versions = isection.versions
        return changed

    @coerced_logic
    def __contains__(self, other):
        # type: (VersionList) -> bool
        if len(self) == 0:
            return False

        for version in other:
            i = bisect_left(self, other)                    # type: ignore[arg-type]
            if i == 0:
                if version not in self[0]:
                    return False
            elif all(
                    version not in v for v in self[i - 1:]  # type: ignore[attr-defined]
            ):
                return False

        return True

    def __getitem__(self, index):
        # type: (Union[int, slice]) -> VersionPredicate
        return self.versions[index]                         # type: ignore[return-value]

    def __iter__(self):
        # type: () -> Iterator[Union[Version, VersionRange]]
        return iter(self.versions)

    def __reversed__(self):
        # type: () -> Iterator[Union[Version, VersionRange]]
        return reversed(self.versions)

    def __len__(self):
        # type: () -> int
        return len(self.versions)

    def __bool__(self):
        # type: () -> bool
        return bool(self.versions)

    @coerced_equals
    def __eq__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, VersionList):
            return NotImplemented
        return self.versions == other.versions

    @coerced_equals
    def __ne__(self, other):
        # type: (VersionList) -> bool
        if not isinstance(other, VersionList):
            return NotImplemented
        return not (self == other)

    @coerced_logic
    def __lt__(self, other):                               # type: ignore[has-type]
        # type: (VersionList) -> bool
        return self.versions < other.versions

    @coerced_logic
    def __le__(self, other):                               # type: ignore[has-type]
        # type: (VersionList) -> bool
        return self == other or self < other

    @coerced_logic
    def __ge__(self, other):
        # type: (VersionList) -> bool
        return self == other or self > other

    @coerced_logic
    def __gt__(self, other):
        # type: (VersionList) -> bool
        return tuple(reversed(self)) > tuple(reversed(other))

    def __hash__(self):
        # type: () -> int
        return hash(tuple(self.versions))

    def __str__(self):
        # type: () -> str
        return ",".join(str(v) for v in self.versions)


def _string_to_version(string):
    # type: (str) -> Union[Version, VersionRange, VersionList]
    """Converts a string to a Version, VersionList, or VersionRange.
       This is private.  Client code should use ver().
    """
    string = string.replace(' ', '')

    if ',' in string:
        return VersionList.parse(string)
    elif ':' in string:
        return VersionRange.parse(string)
    return Version.parse(string)


def ver(obj):
    # type: (Any) -> Union[Version, VersionRange, VersionList]
    """Parses a Version, VersionRange, or VersionList from a string
       or list of strings.
    """
    if isinstance(obj, (list, tuple)):
        return VersionList(obj)                             # type: ignore[arg-type]
    elif isinstance(obj, string_types):
        return ver(_string_to_version(obj))
    elif isinstance(obj, (int, float)):
        return _string_to_version(str(obj))
    elif type(obj) in (Version, VersionRange, VersionList):
        return obj
    else:
        raise TypeError("ver() can't convert %s to version!" % type(obj))


class VersionError(spack.error.SpackError):
    """This is raised when something is wrong with a version."""


class VersionChecksumError(VersionError):
    """Raised for version checksum errors."""
