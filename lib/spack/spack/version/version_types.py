# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import numbers
import re
from bisect import bisect_left
from typing import List, Optional, Tuple, Union

from spack.util.spack_yaml import syaml_dict

from .common import (
    ALPHA,
    COMMIT_VERSION,
    FINAL,
    PRERELEASE_TO_STRING,
    STRING_TO_PRERELEASE,
    EmptyRangeError,
    VersionLookupError,
    infinity_versions,
    is_git_version,
    iv_min_len,
)
from .lookup import AbstractRefLookup

# Valid version characters
VALID_VERSION = re.compile(r"^[A-Za-z0-9_.-][=A-Za-z0-9_.-]*$")

# regex for version segments
SEGMENT_REGEX = re.compile(r"(?:(?P<num>[0-9]+)|(?P<str>[a-zA-Z]+))(?P<sep>[_.-]*)")


class VersionStrComponent:
    __slots__ = ["data"]

    def __init__(self, data):
        # int for infinity index, str for literal.
        self.data: Union[int, str] = data

    @staticmethod
    def from_string(string):
        if len(string) >= iv_min_len:
            try:
                string = infinity_versions.index(string)
            except ValueError:
                pass

        return VersionStrComponent(string)

    def __hash__(self):
        return hash(self.data)

    def __str__(self):
        return (
            ("infinity" if self.data >= len(infinity_versions) else infinity_versions[self.data])
            if isinstance(self.data, int)
            else self.data
        )

    def __repr__(self) -> str:
        return f'VersionStrComponent("{self}")'

    def __eq__(self, other):
        return isinstance(other, VersionStrComponent) and self.data == other.data

    def __lt__(self, other):
        lhs_inf = isinstance(self.data, int)
        if isinstance(other, int):
            return not lhs_inf
        rhs_inf = isinstance(other.data, int)
        return (not lhs_inf and rhs_inf) if lhs_inf ^ rhs_inf else self.data < other.data

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        lhs_inf = isinstance(self.data, int)
        if isinstance(other, int):
            return lhs_inf
        rhs_inf = isinstance(other.data, int)
        return (lhs_inf and not rhs_inf) if lhs_inf ^ rhs_inf else self.data > other.data

    def __ge__(self, other):
        return self > other or self == other


def parse_string_components(string: str) -> Tuple[tuple, tuple]:
    string = string.strip()

    if string and not VALID_VERSION.match(string):
        raise ValueError("Bad characters in version string: %s" % string)

    segments = SEGMENT_REGEX.findall(string)
    separators = tuple(m[2] for m in segments)
    prerelease: Tuple[int, ...]

    # <version>(alpha|beta|rc)<number>
    if len(segments) >= 3 and segments[-2][1] in STRING_TO_PRERELEASE and segments[-1][0]:
        prerelease = (STRING_TO_PRERELEASE[segments[-2][1]], int(segments[-1][0]))
        segments = segments[:-2]

    # <version>(alpha|beta|rc)
    elif len(segments) >= 2 and segments[-1][1] in STRING_TO_PRERELEASE:
        prerelease = (STRING_TO_PRERELEASE[segments[-1][1]],)
        segments = segments[:-1]

    # <version>
    else:
        prerelease = (FINAL,)

    release = tuple(int(m[0]) if m[0] else VersionStrComponent.from_string(m[1]) for m in segments)

    return (release, prerelease), separators


class ConcreteVersion:
    pass


def _stringify_version(versions: Tuple[tuple, tuple], separators: tuple) -> str:
    release, prerelease = versions
    string = ""
    for i in range(len(release)):
        string += f"{release[i]}{separators[i]}"
    if prerelease[0] != FINAL:
        string += f"{PRERELEASE_TO_STRING[prerelease[0]]}{separators[len(release)]}"
        if len(prerelease) > 1:
            string += str(prerelease[1])
    return string


class StandardVersion(ConcreteVersion):
    """Class to represent versions"""

    __slots__ = ["version", "string", "separators"]

    def __init__(self, string: Optional[str], version: Tuple[tuple, tuple], separators: tuple):
        self.string = string
        self.version = version
        self.separators = separators

    @staticmethod
    def from_string(string: str):
        return StandardVersion(string, *parse_string_components(string))

    @staticmethod
    def typemin():
        return _STANDARD_VERSION_TYPEMIN

    @staticmethod
    def typemax():
        return _STANDARD_VERSION_TYPEMAX

    def __bool__(self):
        return True

    def __eq__(self, other):
        if isinstance(other, StandardVersion):
            return self.version == other.version
        return False

    def __ne__(self, other):
        if isinstance(other, StandardVersion):
            return self.version != other.version
        return True

    def __lt__(self, other):
        if isinstance(other, StandardVersion):
            return self.version < other.version
        if isinstance(other, ClosedOpenRange):
            # Use <= here so that Version(x) < ClosedOpenRange(Version(x), ...).
            return self <= other.lo
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, StandardVersion):
            return self.version <= other.version
        if isinstance(other, ClosedOpenRange):
            # Versions are never equal to ranges, so follow < logic.
            return self <= other.lo
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, StandardVersion):
            return self.version >= other.version
        if isinstance(other, ClosedOpenRange):
            # Versions are never equal to ranges, so follow > logic.
            return self > other.lo
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, StandardVersion):
            return self.version > other.version
        if isinstance(other, ClosedOpenRange):
            return self > other.lo
        return NotImplemented

    def __iter__(self):
        return iter(self.version[0])

    def __len__(self):
        return len(self.version[0])

    def __getitem__(self, idx):
        cls = type(self)

        release = self.version[0]

        if isinstance(idx, numbers.Integral):
            return release[idx]

        elif isinstance(idx, slice):
            string_arg = []

            pairs = zip(release[idx], self.separators[idx])
            for token, sep in pairs:
                string_arg.append(str(token))
                string_arg.append(str(sep))

            if string_arg:
                string_arg.pop()  # We don't need the last separator
                string_arg = "".join(string_arg)
                return cls.from_string(string_arg)
            else:
                return StandardVersion.from_string("")

        message = "{cls.__name__} indices must be integers"
        raise TypeError(message.format(cls=cls))

    def __str__(self):
        return self.string or _stringify_version(self.version, self.separators)

    def __repr__(self) -> str:
        # Print indirect repr through Version(...)
        return f'Version("{str(self)}")'

    def __hash__(self):
        # If this is a final release, do not hash the prerelease part for backward compat.
        return hash(self.version if self.is_prerelease() else self.version[0])

    def __contains__(rhs, lhs):
        # We should probably get rid of `x in y` for versions, since
        # versions still have a dual interpretation as singleton sets
        # or elements. x in y should be: is the lhs-element in the
        # rhs-set. Instead this function also does subset checks.
        if isinstance(lhs, (StandardVersion, ClosedOpenRange, VersionList)):
            return lhs.satisfies(rhs)
        raise ValueError(lhs)

    def intersects(self, other: Union["StandardVersion", "GitVersion", "ClosedOpenRange"]) -> bool:
        if isinstance(other, StandardVersion):
            return self == other
        return other.intersects(self)

    def overlaps(self, other) -> bool:
        return self.intersects(other)

    def satisfies(
        self, other: Union["ClosedOpenRange", "StandardVersion", "GitVersion", "VersionList"]
    ) -> bool:
        if isinstance(other, GitVersion):
            return False

        if isinstance(other, StandardVersion):
            return self == other

        if isinstance(other, ClosedOpenRange):
            return other.intersects(self)

        if isinstance(other, VersionList):
            return other.intersects(self)

        return NotImplemented

    def union(self, other: Union["ClosedOpenRange", "StandardVersion"]):
        if isinstance(other, StandardVersion):
            return self if self == other else VersionList([self, other])
        return other.union(self)

    def intersection(self, other: Union["ClosedOpenRange", "StandardVersion"]):
        if isinstance(other, StandardVersion):
            return self if self == other else VersionList()
        return other.intersection(self)

    def isdevelop(self):
        """Triggers on the special case of the `@develop-like` version."""
        return any(
            isinstance(p, VersionStrComponent) and isinstance(p.data, int) for p in self.version[0]
        )

    def is_prerelease(self) -> bool:
        return self.version[1][0] != FINAL

    @property
    def dotted_numeric_string(self) -> str:
        """Replaces all non-numeric components of the version with 0.

        This can be used to pass Spack versions to libraries that have stricter version schema.
        """
        numeric = tuple(0 if isinstance(v, VersionStrComponent) else v for v in self.version[0])
        if self.is_prerelease():
            numeric += (0, *self.version[1][1:])
        return ".".join(str(v) for v in numeric)

    @property
    def dotted(self):
        """The dotted representation of the version.

        Example:
        >>> version = Version('1-2-3b')
        >>> version.dotted
        Version('1.2.3b')

        Returns:
            Version: The version with separator characters replaced by dots
        """
        return type(self).from_string(self.string.replace("-", ".").replace("_", "."))

    @property
    def underscored(self):
        """The underscored representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.underscored
        Version('1_2_3b')

        Returns:
            Version: The version with separator characters replaced by
                underscores
        """
        return type(self).from_string(self.string.replace(".", "_").replace("-", "_"))

    @property
    def dashed(self):
        """The dashed representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.dashed
        Version('1-2-3b')

        Returns:
            Version: The version with separator characters replaced by dashes
        """
        return type(self).from_string(self.string.replace(".", "-").replace("_", "-"))

    @property
    def joined(self):
        """The joined representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.joined
        Version('123b')

        Returns:
            Version: The version with separator characters removed
        """
        return type(self).from_string(
            self.string.replace(".", "").replace("-", "").replace("_", "")
        )

    def up_to(self, index):
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
        return self[:index]


_STANDARD_VERSION_TYPEMIN = StandardVersion("", ((), (ALPHA,)), ("",))

_STANDARD_VERSION_TYPEMAX = StandardVersion(
    "infinity", ((VersionStrComponent(len(infinity_versions)),), (FINAL,)), ("",)
)


class GitVersion(ConcreteVersion):
    """Class to represent versions interpreted from git refs.

    There are two distinct categories of git versions:

    1) GitVersions instantiated with an associated reference version (e.g. 'git.foo=1.2')
    2) GitVersions requiring commit lookups

    Git ref versions that are not paired with a known version are handled separately from
    all other version comparisons. When Spack identifies a git ref version, it associates a
    ``CommitLookup`` object with the version. This object handles caching of information
    from the git repo. When executing comparisons with a git ref version, Spack queries the
    ``CommitLookup`` for the most recent version previous to this git ref, as well as the
    distance between them expressed as a number of commits. If the previous version is
    ``X.Y.Z`` and the distance is ``D``, the git commit version is represented by the
    tuple ``(X, Y, Z, '', D)``. The component ``''`` cannot be parsed as part of any valid
    version, but is a valid component. This allows a git ref version to be less than (older
    than) every Version newer than its previous version, but still newer than its previous
    version.

    To find the previous version from a git ref version, Spack queries the git repo for its
    tags. Any tag that matches a version known to Spack is associated with that version, as
    is any tag that is a known version prepended with the character ``v`` (i.e., a tag
    ``v1.0`` is associated with the known version ``1.0``). Additionally, any tag that
    represents a semver version (X.Y.Z with X, Y, Z all integers) is associated with the
    version it represents, even if that version is not known to Spack. Each tag is then
    queried in git to see whether it is an ancestor of the git ref in question, and if so
    the distance between the two. The previous version is the version that is an ancestor
    with the least distance from the git ref in question.

    This procedure can be circumvented if the user supplies a known version to associate
    with the GitVersion (e.g. ``[hash]=develop``).  If the user prescribes the version then
    there is no need to do a lookup and the standard version comparison operations are
    sufficient.
    """

    __slots__ = ["ref", "has_git_prefix", "is_commit", "_ref_lookup", "_ref_version"]

    def __init__(self, string: str):
        # An object that can lookup git refs to compare them to versions
        self._ref_lookup: Optional[AbstractRefLookup] = None

        # This is the effective version.
        self._ref_version: Optional[StandardVersion]

        self.has_git_prefix = string.startswith("git.")

        # Drop `git.` prefix
        normalized_string = string[4:] if self.has_git_prefix else string

        if "=" in normalized_string:
            # Store the git reference, and parse the user provided version.
            self.ref, spack_version = normalized_string.split("=")
            self._ref_version = StandardVersion(
                spack_version, *parse_string_components(spack_version)
            )
        else:
            # The ref_version is lazily attached after parsing, since we don't know what
            # package it applies to here.
            self._ref_version = None
            self.ref = normalized_string

        # Used by fetcher
        self.is_commit: bool = len(self.ref) == 40 and bool(COMMIT_VERSION.match(self.ref))

    @property
    def ref_version(self) -> StandardVersion:
        # Return cached version if we have it
        if self._ref_version is not None:
            return self._ref_version

        if self.ref_lookup is None:
            raise VersionLookupError(
                f"git ref '{self.ref}' cannot be looked up: " "call attach_lookup first"
            )

        version_string, distance = self.ref_lookup.get(self.ref)
        version_string = version_string or "0"

        # Add a -git.<distance> suffix when we're not exactly on a tag
        if distance > 0:
            version_string += f"-git.{distance}"
        self._ref_version = StandardVersion(
            version_string, *parse_string_components(version_string)
        )
        return self._ref_version

    def intersects(self, other):
        # For concrete things intersects = satisfies = equality
        if isinstance(other, GitVersion):
            return self == other
        if isinstance(other, StandardVersion):
            return False
        if isinstance(other, ClosedOpenRange):
            return self.ref_version.intersects(other)
        if isinstance(other, VersionList):
            return any(self.intersects(rhs) for rhs in other)
        raise ValueError(f"Unexpected type {type(other)}")

    def intersection(self, other):
        if isinstance(other, ConcreteVersion):
            return self if self == other else VersionList()
        return other.intersection(self)

    def overlaps(self, other) -> bool:
        return self.intersects(other)

    def satisfies(
        self, other: Union["GitVersion", StandardVersion, "ClosedOpenRange", "VersionList"]
    ):
        # Concrete versions mean we have to do an equality check
        if isinstance(other, GitVersion):
            return self == other
        if isinstance(other, StandardVersion):
            return False
        if isinstance(other, ClosedOpenRange):
            return self.ref_version.satisfies(other)
        if isinstance(other, VersionList):
            return any(self.satisfies(rhs) for rhs in other)
        raise ValueError(f"Unexpected type {type(other)}")

    def __str__(self):
        s = f"git.{self.ref}" if self.has_git_prefix else self.ref
        # Note: the solver actually depends on str(...) to produce the effective version.
        # So when a lookup is attached, we require the resolved version to be printed.
        # But for standalone git versions that don't have a repo attached, it would still
        # be nice if we could print @<hash>.
        try:
            s += f"={self.ref_version}"
        except VersionLookupError:
            pass
        return s

    def __repr__(self):
        return f'GitVersion("{self}")'

    def __bool__(self):
        return True

    def __eq__(self, other):
        # GitVersion cannot be equal to StandardVersion, otherwise == is not transitive
        return (
            isinstance(other, GitVersion)
            and self.ref == other.ref
            and self.ref_version == other.ref_version
        )

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, GitVersion):
            return (self.ref_version, self.ref) < (other.ref_version, other.ref)
        if isinstance(other, StandardVersion):
            # GitVersion at equal ref version is larger than StandardVersion
            return self.ref_version < other
        if isinstance(other, ClosedOpenRange):
            return self.ref_version < other
        raise ValueError(f"Unexpected type {type(other)}")

    def __le__(self, other):
        if isinstance(other, GitVersion):
            return (self.ref_version, self.ref) <= (other.ref_version, other.ref)
        if isinstance(other, StandardVersion):
            # Note: GitVersion hash=1.2.3 > StandardVersion 1.2.3, so use < comparsion.
            return self.ref_version < other
        if isinstance(other, ClosedOpenRange):
            # Equality is not a thing
            return self.ref_version < other
        raise ValueError(f"Unexpected type {type(other)}")

    def __ge__(self, other):
        if isinstance(other, GitVersion):
            return (self.ref_version, self.ref) >= (other.ref_version, other.ref)
        if isinstance(other, StandardVersion):
            # Note: GitVersion hash=1.2.3 > StandardVersion 1.2.3, so use >= here.
            return self.ref_version >= other
        if isinstance(other, ClosedOpenRange):
            return self.ref_version > other
        raise ValueError(f"Unexpected type {type(other)}")

    def __gt__(self, other):
        if isinstance(other, GitVersion):
            return (self.ref_version, self.ref) > (other.ref_version, other.ref)
        if isinstance(other, StandardVersion):
            # Note: GitVersion hash=1.2.3 > StandardVersion 1.2.3, so use >= here.
            return self.ref_version >= other
        if isinstance(other, ClosedOpenRange):
            return self.ref_version > other
        raise ValueError(f"Unexpected type {type(other)}")

    def __hash__(self):
        # hashing should not cause version lookup
        return hash(self.ref)

    def __contains__(self, other):
        raise Exception("Not implemented yet")

    @property
    def ref_lookup(self):
        if self._ref_lookup:
            # Get operation ensures dict is populated
            self._ref_lookup.get(self.ref)
            return self._ref_lookup

    def attach_lookup(self, lookup: AbstractRefLookup):
        """
        Use the git fetcher to look up a version for a commit.

        Since we want to optimize the clone and lookup, we do the clone once
        and store it in the user specified git repository cache. We also need
        context of the package to get known versions, which could be tags if
        they are linked to Git Releases. If we are unable to determine the
        context of the version, we cannot continue. This implementation is
        alongside the GitFetcher because eventually the git repos cache will
        be one and the same with the source cache.
        """
        self._ref_lookup = lookup

    def __iter__(self):
        return self.ref_version.__iter__()

    def __len__(self):
        return self.ref_version.__len__()

    def __getitem__(self, idx):
        return self.ref_version.__getitem__(idx)

    def isdevelop(self):
        return self.ref_version.isdevelop()

    def is_prerelease(self) -> bool:
        return self.ref_version.is_prerelease()

    @property
    def dotted(self) -> StandardVersion:
        return self.ref_version.dotted

    @property
    def underscored(self) -> StandardVersion:
        return self.ref_version.underscored

    @property
    def dashed(self) -> StandardVersion:
        return self.ref_version.dashed

    @property
    def joined(self) -> StandardVersion:
        return self.ref_version.joined

    def up_to(self, index) -> StandardVersion:
        return self.ref_version.up_to(index)


class ClosedOpenRange:
    def __init__(self, lo: StandardVersion, hi: StandardVersion):
        if hi < lo:
            raise EmptyRangeError(f"{lo}..{hi} is an empty range")
        self.lo: StandardVersion = lo
        self.hi: StandardVersion = hi

    @classmethod
    def from_version_range(cls, lo: StandardVersion, hi: StandardVersion):
        """Construct ClosedOpenRange from lo:hi range."""
        try:
            return ClosedOpenRange(lo, _next_version(hi))
        except EmptyRangeError as e:
            raise EmptyRangeError(f"{lo}:{hi} is an empty range") from e

    def __str__(self):
        # This simplifies 3.1:<3.2 to 3.1:3.1 to 3.1
        # 3:3 -> 3
        hi_prev = _prev_version(self.hi)
        if self.lo != StandardVersion.typemin() and self.lo == hi_prev:
            return str(self.lo)
        lhs = "" if self.lo == StandardVersion.typemin() else str(self.lo)
        rhs = "" if hi_prev == StandardVersion.typemax() else str(hi_prev)
        return f"{lhs}:{rhs}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        # prev_version for backward compat.
        return hash((self.lo, _prev_version(self.hi)))

    def __eq__(self, other):
        if isinstance(other, StandardVersion):
            return False
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) == (other.lo, other.hi)
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, StandardVersion):
            return True
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) != (other.lo, other.hi)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, StandardVersion):
            return other > self
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) < (other.lo, other.hi)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, StandardVersion):
            return other >= self
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) <= (other.lo, other.hi)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, StandardVersion):
            return other <= self
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) >= (other.lo, other.hi)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, StandardVersion):
            return other < self
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) > (other.lo, other.hi)
        return NotImplemented

    def __contains__(rhs, lhs):
        if isinstance(lhs, (ConcreteVersion, ClosedOpenRange, VersionList)):
            return lhs.satisfies(rhs)
        raise ValueError(f"Unexpected type {type(lhs)}")

    def intersects(self, other: Union[ConcreteVersion, "ClosedOpenRange", "VersionList"]):
        if isinstance(other, StandardVersion):
            return self.lo <= other < self.hi
        if isinstance(other, GitVersion):
            return self.lo <= other.ref_version < self.hi
        if isinstance(other, ClosedOpenRange):
            return (self.lo < other.hi) and (other.lo < self.hi)
        if isinstance(other, VersionList):
            return any(self.intersects(rhs) for rhs in other)
        raise ValueError(f"Unexpected type {type(other)}")

    def satisfies(self, other: Union["ClosedOpenRange", ConcreteVersion, "VersionList"]):
        if isinstance(other, ConcreteVersion):
            return False
        if isinstance(other, ClosedOpenRange):
            return not (self.lo < other.lo or other.hi < self.hi)
        if isinstance(other, VersionList):
            return any(self.satisfies(rhs) for rhs in other)
        raise ValueError(other)

    def overlaps(self, other: Union["ClosedOpenRange", ConcreteVersion, "VersionList"]) -> bool:
        return self.intersects(other)

    def _union_if_not_disjoint(
        self, other: Union["ClosedOpenRange", ConcreteVersion]
    ) -> Optional["ClosedOpenRange"]:
        """Same as union, but returns None when the union is not connected. This function is not
        implemented for version lists as right-hand side, as that makes little sense."""
        if isinstance(other, StandardVersion):
            return self if self.lo <= other < self.hi else None

        if isinstance(other, GitVersion):
            return self if self.lo <= other.ref_version < self.hi else None

        if isinstance(other, ClosedOpenRange):
            # Notice <= cause we want union(1:2, 3:4) = 1:4.
            return (
                ClosedOpenRange(min(self.lo, other.lo), max(self.hi, other.hi))
                if self.lo <= other.hi and other.lo <= self.hi
                else None
            )

        raise TypeError(f"Unexpected type {type(other)}")

    def union(self, other: Union["ClosedOpenRange", ConcreteVersion, "VersionList"]):
        if isinstance(other, VersionList):
            v = other.copy()
            v.add(self)
            return v

        result = self._union_if_not_disjoint(other)
        return result if result is not None else VersionList([self, other])

    def intersection(self, other: Union["ClosedOpenRange", ConcreteVersion]):
        # range - version -> singleton or nothing.
        if isinstance(other, ConcreteVersion):
            return other if self.intersects(other) else VersionList()

        # range - range -> range or nothing.
        max_lo = max(self.lo, other.lo)
        min_hi = min(self.hi, other.hi)
        return ClosedOpenRange(max_lo, min_hi) if max_lo < min_hi else VersionList()


class VersionList:
    """Sorted, non-redundant list of Version and ClosedOpenRange elements."""

    def __init__(self, vlist=None):
        self.versions: List[Union[StandardVersion, GitVersion, ClosedOpenRange]] = []
        if vlist is None:
            pass
        elif isinstance(vlist, str):
            vlist = from_string(vlist)
            if isinstance(vlist, VersionList):
                self.versions = vlist.versions
            else:
                self.versions = [vlist]
        else:
            for v in vlist:
                self.add(ver(v))

    def add(self, item: Union[StandardVersion, GitVersion, ClosedOpenRange, "VersionList"]):
        if isinstance(item, (StandardVersion, GitVersion)):
            i = bisect_left(self, item)
            # Only insert when prev and next are not intersected.
            if (i == 0 or not item.intersects(self[i - 1])) and (
                i == len(self) or not item.intersects(self[i])
            ):
                self.versions.insert(i, item)

        elif isinstance(item, ClosedOpenRange):
            i = bisect_left(self, item)

            # Note: can span multiple concrete versions to the left (as well as to the right).
            # For instance insert 1.2: into [1.2, hash=1.2, 1.3, 1.4:1.5]
            # would bisect at i = 1 and merge i = 0 too.
            while i > 0:
                union = item._union_if_not_disjoint(self[i - 1])
                if union is None:  # disjoint
                    break
                item = union
                del self.versions[i - 1]
                i -= 1

            while i < len(self):
                union = item._union_if_not_disjoint(self[i])
                if union is None:
                    break
                item = union
                del self.versions[i]

            self.versions.insert(i, item)

        elif isinstance(item, VersionList):
            for v in item:
                self.add(v)

        else:
            raise TypeError("Can't add %s to VersionList" % type(item))

    @property
    def concrete(self) -> Optional[ConcreteVersion]:
        return self[0] if len(self) == 1 and isinstance(self[0], ConcreteVersion) else None

    @property
    def concrete_range_as_version(self) -> Optional[ConcreteVersion]:
        """Like concrete, but collapses VersionRange(x, x) to Version(x).
        This is just for compatibility with old Spack."""
        if len(self) != 1:
            return None
        v = self[0]
        if isinstance(v, ConcreteVersion):
            return v
        if isinstance(v, ClosedOpenRange) and _next_version(v.lo) == v.hi:
            return v.lo
        return None

    def copy(self):
        return VersionList(self)

    def lowest(self) -> Optional[StandardVersion]:
        """Get the lowest version in the list."""
        return next((v for v in self.versions if isinstance(v, StandardVersion)), None)

    def highest(self) -> Optional[StandardVersion]:
        """Get the highest version in the list."""
        return next((v for v in reversed(self.versions) if isinstance(v, StandardVersion)), None)

    def highest_numeric(self) -> Optional[StandardVersion]:
        """Get the highest numeric version in the list."""
        numeric = (
            v
            for v in reversed(self.versions)
            if isinstance(v, StandardVersion) and not v.isdevelop()
        )
        return next(numeric, None)

    def preferred(self) -> Optional[StandardVersion]:
        """Get the preferred (latest) version in the list."""
        return self.highest_numeric() or self.highest()

    def satisfies(self, other) -> bool:
        # This exploits the fact that version lists are "reduced" and normalized, so we can
        # never have a list like [1:3, 2:4] since that would be normalized to [1:4]
        if isinstance(other, VersionList):
            return all(any(lhs.satisfies(rhs) for rhs in other) for lhs in self)

        if isinstance(other, (ConcreteVersion, ClosedOpenRange)):
            return all(lhs.satisfies(other) for lhs in self)

        raise ValueError(f"Unsupported type {type(other)}")

    def intersects(self, other):
        if isinstance(other, VersionList):
            s = o = 0
            while s < len(self) and o < len(other):
                if self[s].intersects(other[o]):
                    return True
                elif self[s] < other[o]:
                    s += 1
                else:
                    o += 1
            return False

        if isinstance(other, (ClosedOpenRange, StandardVersion)):
            return any(v.intersects(other) for v in self)

        raise ValueError(f"Unsupported type {type(other)}")

    def overlaps(self, other) -> bool:
        return self.intersects(other)

    def to_dict(self):
        """Generate human-readable dict for YAML."""
        if self.concrete:
            return syaml_dict([("version", str(self[0]))])
        return syaml_dict([("versions", [str(v) for v in self])])

    @staticmethod
    def from_dict(dictionary):
        """Parse dict from to_dict."""
        if "versions" in dictionary:
            return VersionList(dictionary["versions"])
        elif "version" in dictionary:
            return VersionList([Version(dictionary["version"])])
        raise ValueError("Dict must have 'version' or 'versions' in it.")

    def update(self, other: "VersionList"):
        for v in other.versions:
            self.add(v)

    def union(self, other: "VersionList"):
        result = self.copy()
        result.update(other)
        return result

    def intersection(self, other: "VersionList") -> "VersionList":
        result = VersionList()
        for lhs, rhs in ((self, other), (other, self)):
            for x in lhs:
                i = bisect_left(rhs.versions, x)
                if i > 0:
                    result.add(rhs[i - 1].intersection(x))
                if i < len(rhs):
                    result.add(rhs[i].intersection(x))
        return result

    def intersect(self, other) -> bool:
        """Intersect this spec's list with other.

        Return True if the spec changed as a result; False otherwise
        """
        isection = self.intersection(other)
        changed = isection.versions != self.versions
        self.versions = isection.versions
        return changed

    def __contains__(self, other):
        if isinstance(other, (ClosedOpenRange, StandardVersion)):
            i = bisect_left(self, other)
            return (i > 0 and other in self[i - 1]) or (i < len(self) and other in self[i])

        if isinstance(other, VersionList):
            return all(item in self for item in other)

        return False

    def __getitem__(self, index):
        return self.versions[index]

    def __iter__(self):
        return iter(self.versions)

    def __reversed__(self):
        return reversed(self.versions)

    def __len__(self):
        return len(self.versions)

    def __bool__(self):
        return bool(self.versions)

    def __eq__(self, other):
        if isinstance(other, VersionList):
            return self.versions == other.versions
        return False

    def __ne__(self, other):
        if isinstance(other, VersionList):
            return self.versions != other.versions
        return False

    def __lt__(self, other):
        if isinstance(other, VersionList):
            return self.versions < other.versions
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, VersionList):
            return self.versions <= other.versions
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, VersionList):
            return self.versions >= other.versions
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, VersionList):
            return self.versions > other.versions
        return NotImplemented

    def __hash__(self):
        return hash(tuple(self.versions))

    def __str__(self):
        if not self.versions:
            return ""

        return ",".join(
            f"={v}" if isinstance(v, StandardVersion) else str(v) for v in self.versions
        )

    def __repr__(self):
        return str(self.versions)


def _next_str(s: str) -> str:
    """Produce the next string of A-Z and a-z characters"""
    return (
        (s + "A")
        if (len(s) == 0 or s[-1] == "z")
        else s[:-1] + ("a" if s[-1] == "Z" else chr(ord(s[-1]) + 1))
    )


def _prev_str(s: str) -> str:
    """Produce the previous string of A-Z and a-z characters"""
    return (
        s[:-1]
        if (len(s) == 0 or s[-1] == "A")
        else s[:-1] + ("Z" if s[-1] == "a" else chr(ord(s[-1]) - 1))
    )


def _next_version_str_component(v: VersionStrComponent) -> VersionStrComponent:
    """
    Produce the next VersionStrComponent, where
    masteq -> mastes
    master -> main
    """
    # First deal with the infinity case.
    data = v.data
    if isinstance(data, int):
        return VersionStrComponent(data + 1)

    # Find the next non-infinity string.
    while True:
        data = _next_str(data)
        if data not in infinity_versions:
            break

    return VersionStrComponent(data)


def _prev_version_str_component(v: VersionStrComponent) -> VersionStrComponent:
    """
    Produce the previous VersionStrComponent, where
    mastes -> masteq
    master -> head
    """
    # First deal with the infinity case. Allow underflows
    data = v.data
    if isinstance(data, int):
        return VersionStrComponent(data - 1)

    # Find the next string.
    while True:
        data = _prev_str(data)
        if data not in infinity_versions:
            break

    return VersionStrComponent(data)


def _next_version(v: StandardVersion) -> StandardVersion:
    release, prerelease = v.version
    separators = v.separators
    prerelease_type = prerelease[0]
    if prerelease_type != FINAL:
        prerelease = (prerelease_type, prerelease[1] + 1 if len(prerelease) > 1 else 0)
    elif len(release) == 0:
        release = (VersionStrComponent("A"),)
        separators = ("",)
    elif isinstance(release[-1], VersionStrComponent):
        release = release[:-1] + (_next_version_str_component(release[-1]),)
    else:
        release = release[:-1] + (release[-1] + 1,)
    components = [""] * (2 * len(release))
    components[::2] = release
    components[1::2] = separators[: len(release)]
    if prerelease_type != FINAL:
        components.extend((PRERELEASE_TO_STRING[prerelease_type], prerelease[1]))
    return StandardVersion("".join(str(c) for c in components), (release, prerelease), separators)


def _prev_version(v: StandardVersion) -> StandardVersion:
    # this function does not deal with underflow, because it's always called as
    # _prev_version(_next_version(v)).
    release, prerelease = v.version
    separators = v.separators
    prerelease_type = prerelease[0]
    if prerelease_type != FINAL:
        prerelease = (
            (prerelease_type,) if prerelease[1] == 0 else (prerelease_type, prerelease[1] - 1)
        )
    elif len(release) == 0:
        return v
    elif isinstance(release[-1], VersionStrComponent):
        release = release[:-1] + (_prev_version_str_component(release[-1]),)
    else:
        release = release[:-1] + (release[-1] - 1,)
    components = [""] * (2 * len(release))
    components[::2] = release
    components[1::2] = separators[: len(release)]
    if prerelease_type != FINAL:
        components.extend((PRERELEASE_TO_STRING[prerelease_type], *prerelease[1:]))

    # this is only used for comparison functions, so don't bother making a string
    return StandardVersion(None, (release, prerelease), separators)


def Version(string: Union[str, int]) -> Union[GitVersion, StandardVersion]:
    if not isinstance(string, (str, int)):
        raise ValueError(f"Cannot construct a version from {type(string)}")
    string = str(string)
    if is_git_version(string):
        return GitVersion(string)
    return StandardVersion.from_string(str(string))


def VersionRange(lo: Union[str, StandardVersion], hi: Union[str, StandardVersion]):
    lo = lo if isinstance(lo, StandardVersion) else StandardVersion.from_string(lo)
    hi = hi if isinstance(hi, StandardVersion) else StandardVersion.from_string(hi)
    return ClosedOpenRange.from_version_range(lo, hi)


def from_string(string) -> Union[VersionList, ClosedOpenRange, StandardVersion, GitVersion]:
    """Converts a string to a version object. This is private. Client code should use ver()."""
    string = string.replace(" ", "")

    # VersionList
    if "," in string:
        return VersionList(list(map(from_string, string.split(","))))

    # ClosedOpenRange
    elif ":" in string:
        s, e = string.split(":")
        lo = StandardVersion.typemin() if s == "" else StandardVersion.from_string(s)
        hi = StandardVersion.typemax() if e == "" else StandardVersion.from_string(e)
        return VersionRange(lo, hi)

    # StandardVersion
    elif string.startswith("="):
        # @=1.2.3 is an exact version
        return Version(string[1:])

    elif is_git_version(string):
        return GitVersion(string)

    else:
        # @1.2.3 is short for 1.2.3:1.2.3
        v = StandardVersion.from_string(string)
        return VersionRange(v, v)


def ver(obj) -> Union[VersionList, ClosedOpenRange, StandardVersion, GitVersion]:
    """Parses a Version, VersionRange, or VersionList from a string
    or list of strings.
    """
    if isinstance(obj, (list, tuple)):
        return VersionList(obj)
    elif isinstance(obj, str):
        return from_string(obj)
    elif isinstance(obj, (int, float)):
        return from_string(str(obj))
    elif isinstance(obj, (StandardVersion, GitVersion, ClosedOpenRange, VersionList)):
        return obj
    else:
        raise TypeError("ver() can't convert %s to version!" % type(obj))
