# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module implements Version and version-ish objects.  These are:

StandardVersion: A single version of a package.
ClosedOpenRange: A range of versions of a package.
VersionList: A ordered list of Version and VersionRange elements.

The set of Version and ClosedOpenRange is totally ordered wiht <
defined as Version(x) < VersionRange(Version(y), Version(x))
if Version(x) <= Version(y).
"""
import numbers
import os
import re
from bisect import bisect_left
from typing import Dict, List, Optional, Tuple, Union

from llnl.util.filesystem import mkdirp, working_dir

import spack.caches
import spack.error
import spack.paths
import spack.util.executable
import spack.util.spack_json as sjson
import spack.util.url
from spack.util.spack_yaml import syaml_dict

# Valid version characters
VALID_VERSION = re.compile(r"^[A-Za-z0-9_.-][=A-Za-z0-9_.-]*$")

# regex for a commit version
COMMIT_VERSION = re.compile(r"^[a-f0-9]{40}$")

# regex for version segments
SEGMENT_REGEX = re.compile(r"(?:(?P<num>[0-9]+)|(?P<str>[a-zA-Z]+))(?P<sep>[_.-]*)")

# regular expression for semantic versioning
SEMVER_REGEX = re.compile(
    ".+(?P<semver>([0-9]+)[.]([0-9]+)[.]([0-9]+)"
    "(?:-([0-9A-Za-z-]+(?:[.][0-9A-Za-z-]+)*))?"
    "(?:[+][0-9A-Za-z-]+)?)"
)

# Infinity-like versions. The order in the list implies the comparison rules
infinity_versions = ["stable", "trunk", "head", "master", "main", "develop"]

iv_min_len = min(len(s) for s in infinity_versions)


class VersionStrComponent(object):
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
    version = tuple(int(m[0]) if m[0] else VersionStrComponent.from_string(m[1]) for m in segments)
    separators = tuple(m[2] for m in segments)
    return version, separators


class ConcreteVersion:
    pass


class StandardVersion(ConcreteVersion):
    """Class to represent versions"""

    __slots__ = ["version", "string", "separators"]

    def __init__(self, string: Optional[str], version: tuple, separators: tuple):
        self.string = string
        self.version = version
        self.separators = separators

    @staticmethod
    def from_string(string: str):
        return StandardVersion(string, *parse_string_components(string))

    @staticmethod
    def typemin():
        return StandardVersion("", (), ())

    @staticmethod
    def typemax():
        return StandardVersion("infinity", (VersionStrComponent(len(infinity_versions)),), ())

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
        return iter(self.version)

    def __len__(self):
        return len(self.version)

    def __getitem__(self, idx):
        cls = type(self)

        if isinstance(idx, numbers.Integral):
            return self.version[idx]

        elif isinstance(idx, slice):
            string_arg = []

            pairs = zip(self.version[idx], self.separators[idx])
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
        return (
            self.string
            if isinstance(self.string, str)
            else ".".join((str(c) for c in self.version))
        )

    def __repr__(self) -> str:
        # Print indirect repr through Version(...)
        return f'Version("{str(self)}")'

    def __hash__(self):
        return hash(self.version)

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
            isinstance(p, VersionStrComponent) and isinstance(p.data, int) for p in self.version
        )

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

    def __init__(self, string: str):
        # An object that can lookup git refs to compare them to versions
        self._ref_lookup: Optional[CommitLookup] = None

        # This is the effective version.
        self._ref_version: Optional[StandardVersion]

        # Drop `git.` prefix
        self.normalized_string = string[4:] if string.startswith("git.") else string
        self.string = string

        if "=" in self.normalized_string:
            # User has supplied a version to associate with this git ref
            self.user_supplied_reference = True

            # Store the git reference, and parse the user provided version.
            self.ref, spack_version = self.normalized_string.split("=")
            self._ref_version = StandardVersion(
                spack_version, *parse_string_components(spack_version)
            )
        else:
            self.user_supplied_reference = False
            # The ref_version is lazily attached after parsing, since we don't know what
            # package it applies to here.
            self._ref_version = None
            self.ref = self.normalized_string

        # Used by fetcher
        self.is_commit: bool = bool(len(self.ref) == 40 and COMMIT_VERSION.match(self.ref))

    @property
    def ref_version(self) -> StandardVersion:
        # Return cached version if we have it
        if self._ref_version is not None:
            return self._ref_version

        if self.ref_lookup is None:
            raise RuntimeError(
                f"git ref '{self.ref}' cannot be looked up: "
                "call attach_git_lookup_from_package first"
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
        return f"{self.ref}={self.ref_version}"

    def __repr__(self):
        return "GitVersion(" + repr(self.string) + ")"

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

    def is_predecessor(self, other: "GitVersion"):
        """True if the other version is the immediate predecessor of this one.
        That is, NO non-commit versions v exist such that:
        (self < v < other and v not in self).
        """
        if not isinstance(other, GitVersion):
            raise ValueError("Needs a GitVersion to compare to")

        if self.ref_version[:-1] != other.ref_version[:-1]:
            return False

        sl = self.ref_version[-1]
        ol = other.ref_version[-1]
        return type(sl) == int and type(ol) == int and (ol - sl == 1)

    @property
    def ref_lookup(self):
        if self._ref_lookup:
            # Get operation ensures dict is populated
            self._ref_lookup.get(self.ref)
            return self._ref_lookup

    def attach_git_lookup_from_package(self, pkg_name):
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
        self._ref_lookup = self._ref_lookup or CommitLookup(pkg_name)


class ClosedOpenRange:
    def __init__(self, lo: StandardVersion, hi: StandardVersion):
        if hi < lo:
            raise ValueError(f"{lo}:{hi} is an empty range")
        self.lo: StandardVersion = lo
        self.hi: StandardVersion = hi

    @classmethod
    def from_version_range(cls, lo: StandardVersion, hi: StandardVersion):
        """Construct ClosedOpenRange from lo:hi range."""
        return ClosedOpenRange(lo, next_version(hi))

    def __str__(self):
        # This simplifies 3.1:<3.2 to 3.1:3.1 to 3.1
        # 3:3 -> 3
        hi_prev = prev_version(self.hi)
        if self.lo != StandardVersion.typemin() and self.lo == hi_prev:
            return str(self.lo)
        lhs = "" if self.lo == StandardVersion.typemin() else str(self.lo)
        rhs = "" if hi_prev == StandardVersion.typemax() else str(hi_prev)
        return f"{lhs}:{rhs}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        # prev_version for backward compat.
        return hash((self.lo, prev_version(self.hi)))

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

    def __contains__(rhs, lhs: Union[StandardVersion, "ClosedOpenRange", "VersionList"]):
        # We should probably get rid of `x in y` for versions, since
        # versions still have a dual interpretation as singleton sets
        # or elements. x in y should be: is the lhs-element in the
        # rhs-set. Instead this function also does subset checks.
        if isinstance(lhs, (StandardVersion, ClosedOpenRange, VersionList)):
            return lhs.satisfies(rhs)
        raise ValueError(lhs)

    def intersects(self, other: Union[StandardVersion, "ClosedOpenRange", "VersionList"]):
        if isinstance(other, StandardVersion):
            return self.lo <= other < self.hi
        if isinstance(other, GitVersion):
            return self.lo <= other.ref_version < self.hi
        if isinstance(other, ClosedOpenRange):
            return (self.lo < other.hi) and (other.lo < self.hi)
        if isinstance(other, VersionList):
            return any(self.intersects(rhs) for rhs in other)
        raise ValueError(other)

    def satisfies(
        self, other: Union["ClosedOpenRange", GitVersion, StandardVersion, "VersionList"]
    ):
        if isinstance(other, ConcreteVersion):
            return False
        if isinstance(other, ClosedOpenRange):
            return not (self.lo < other.lo or other.hi < self.hi)
        if isinstance(other, VersionList):
            return any(self.satisfies(rhs) for rhs in other)
        raise ValueError(other)

    def overlaps(self, other: Union["ClosedOpenRange", StandardVersion, "VersionList"]) -> bool:
        return self.intersects(other)

    def union(self, other: Union["ClosedOpenRange", StandardVersion, GitVersion, "VersionList"]):
        if isinstance(other, StandardVersion):
            return self if self.lo <= other < self.hi else VersionList([self, other])

        if isinstance(other, GitVersion):
            return self if self.lo <= other.ref_version < self.hi else VersionList([self, other])

        if isinstance(other, ClosedOpenRange):
            # Notice <= cause we want union(1:2, 3:4) = 1:4.
            if (self.lo <= other.hi) and (other.lo <= self.hi):
                return ClosedOpenRange(min(self.lo, other.lo), max(self.hi, other.hi))

            return VersionList([self, other])

        if isinstance(other, VersionList):
            v = other.copy()
            v.add(self)
            return v

        raise ValueError(f"Unexpected type {type(other)}")

    def intersection(self, other: Union["ClosedOpenRange", StandardVersion]):
        # range - version -> singleton or nothing.
        if isinstance(other, StandardVersion):
            return other if self.intersects(other) else VersionList()

        # range - range -> range or nothing.
        max_lo = max(self.lo, other.lo)
        min_hi = min(self.hi, other.hi)
        return ClosedOpenRange(max_lo, min_hi) if max_lo < min_hi else VersionList()


class VersionList:
    """Sorted, non-redundant list of Version and ClosedOpenRange elements."""

    def __init__(self, vlist=None):
        self.versions: List[StandardVersion, GitVersion, ClosedOpenRange] = []
        if vlist is not None:
            if isinstance(vlist, str):
                vlist = from_string(vlist)
                if type(vlist) == VersionList:
                    self.versions = vlist.versions
                else:
                    self.versions = [vlist]
            else:
                for v in vlist:
                    self.add(ver(v))

    def add(self, item):
        if isinstance(item, ConcreteVersion):
            i = bisect_left(self, item)
            # Only insert when prev and next are not intersected.
            if (i == 0 or not item.intersects(self[i - 1])) and (
                i == len(self) or not item.intersects(self[i])
            ):
                self.versions.insert(i, item)

        elif isinstance(item, ClosedOpenRange):
            i = bisect_left(self, item)

            # Note: can span multiple concrete versions to the left,
            # For instance insert 1.2: into [1.2, hash=1.2, 1.3]
            # would bisect to i = 1.
            while i > 0 and item.intersects(self[i - 1]):
                item = item.union(self[i - 1])
                del self.versions[i - 1]
                i -= 1

            while i < len(self) and item.intersects(self[i]):
                item = item.union(self[i])
                del self.versions[i]

            self.versions.insert(i, item)

        elif type(item) == VersionList:
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
        if isinstance(v, ClosedOpenRange) and next_version(v.lo) == v.hi:
            return v.lo
        return None

    def copy(self):
        return VersionList(self)

    def lowest(self) -> Optional[StandardVersion]:
        """Get the lowest version in the list."""
        return None if not self else self[0]

    def highest(self) -> Optional[StandardVersion]:
        """Get the highest version in the list."""
        return None if not self else self[-1]

    def highest_numeric(self) -> Optional[StandardVersion]:
        """Get the highest numeric version in the list."""
        numeric_versions = list(filter(lambda v: str(v) not in infinity_versions, self.versions))
        return None if not any(numeric_versions) else numeric_versions[-1]

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
        return ",".join(str(v) for v in self.versions)

    def __repr__(self):
        return str(self.versions)


def next_str(s: str) -> str:
    """Produce the next string of A-Z and a-z characters"""
    return (
        (s + "A")
        if (len(s) == 0 or s[-1] == "z")
        else s[:-1] + ("a" if s[-1] == "Z" else chr(ord(s[-1]) + 1))
    )


def prev_str(s: str) -> str:
    """Produce the previous string of A-Z and a-z characters"""
    return (
        s[:-1]
        if (len(s) == 0 or s[-1] == "A")
        else s[:-1] + ("Z" if s[-1] == "a" else chr(ord(s[-1]) - 1))
    )


def next_version_str_component(v: VersionStrComponent) -> VersionStrComponent:
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
        data = next_str(data)
        if data not in infinity_versions:
            break

    return VersionStrComponent(data)


def prev_version_str_component(v: VersionStrComponent) -> VersionStrComponent:
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
        data = prev_str(data)
        if data not in infinity_versions:
            break

    return VersionStrComponent(data)


def next_version(v: StandardVersion) -> StandardVersion:
    if len(v.version) == 0:
        nxt = VersionStrComponent("A")
    elif isinstance(v.version[-1], VersionStrComponent):
        nxt = next_version_str_component(v.version[-1])
    else:
        nxt = v.version[-1] + 1

    # Construct a string-version for printing
    string_components = []
    for part, sep in zip(v.version[:-1], v.separators):
        string_components.append(str(part))
        string_components.append(str(sep))
    string_components.append(str(nxt))

    return StandardVersion("".join(string_components), v.version[:-1] + (nxt,), v.separators)


def prev_version(v: StandardVersion) -> StandardVersion:
    if len(v.version) == 0:
        return v
    elif isinstance(v.version[-1], VersionStrComponent):
        prev = prev_version_str_component(v.version[-1])
    else:
        prev = v.version[-1] - 1

    # Construct a string-version for printing
    string_components = []
    for part, sep in zip(v.version[:-1], v.separators):
        string_components.append(str(part))
        string_components.append(str(sep))
    string_components.append(str(prev))

    return StandardVersion("".join(string_components), v.version[:-1] + (prev,), v.separators)


def is_git_version(string: str) -> bool:
    return bool(
        string.startswith("git.")
        or len(string) == 40
        and COMMIT_VERSION.match(string)
        or "=" in string[1:]
    )


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
    """Converts a string to a version object.
    This is private. Client code should use ver()."""
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


class VersionError(spack.error.SpackError):
    """This is raised when something is wrong with a version."""


class VersionChecksumError(VersionError):
    """Raised for version checksum errors."""


class VersionLookupError(VersionError):
    """Raised for errors looking up git commits as versions."""


class CommitLookup(object):
    """An object for cached lookups of git commits

    CommitLookup objects delegate to the misc_cache for locking. CommitLookup objects may
    be attached to a GitVersion to allow for comparisons between git refs and versions as
    represented by tags in the git repository.
    """

    def __init__(self, pkg_name):
        self.pkg_name = pkg_name

        self.data: Dict[str, Tuple[Optional[str], int]] = {}

        self._pkg = None
        self._fetcher = None
        self._cache_key = None
        self._cache_path = None

    # The following properties are used as part of a lazy reference scheme
    # to avoid querying the package repository until it is necessary (and
    # in particular to wait until after the configuration has been
    # assembled)
    @property
    def cache_key(self):
        if not self._cache_key:
            key_base = "git_metadata"
            if not self.repository_uri.startswith("/"):
                key_base += "/"
            self._cache_key = key_base + self.repository_uri

            # Cache data in misc_cache
            # If this is the first lazy access, initialize the cache as well
            spack.caches.misc_cache.init_entry(self.cache_key)
        return self._cache_key

    @property
    def cache_path(self):
        if not self._cache_path:
            self._cache_path = spack.caches.misc_cache.cache_path(self.cache_key)
        return self._cache_path

    @property
    def pkg(self):
        if not self._pkg:
            import spack.repo  # break cycle

            self._pkg = spack.repo.path.get_pkg_class(self.pkg_name)
        return self._pkg

    @property
    def fetcher(self):
        if not self._fetcher:
            # We require the full git repository history
            import spack.fetch_strategy  # break cycle

            fetcher = spack.fetch_strategy.GitFetchStrategy(git=self.pkg.git)
            fetcher.get_full_repo = True
            self._fetcher = fetcher
        return self._fetcher

    @property
    def repository_uri(self):
        """Identifier for git repos used within the repo and metadata caches."""
        try:
            components = [
                str(c).lstrip("/") for c in spack.util.url.parse_git_url(self.pkg.git) if c
            ]
            return os.path.join(*components)
        except ValueError:
            # If it's not a git url, it's a local path
            return os.path.abspath(self.pkg.git)

    def save(self):
        """Save the data to file"""
        with spack.caches.misc_cache.write_transaction(self.cache_key) as (old, new):
            sjson.dump(self.data, new)

    def load_data(self):
        """Load data if the path already exists."""
        if os.path.isfile(self.cache_path):
            with spack.caches.misc_cache.read_transaction(self.cache_key) as cache_file:
                self.data = sjson.load(cache_file)

    def get(self, ref) -> Tuple[Optional[str], int]:
        if not self.data:
            self.load_data()

        if ref not in self.data:
            self.data[ref] = self.lookup_ref(ref)
            self.save()

        return self.data[ref]

    def lookup_ref(self, ref) -> Tuple[Optional[str], int]:
        """Lookup the previous version and distance for a given commit.

        We use git to compare the known versions from package to the git tags,
        as well as any git tags that are SEMVER versions, and find the latest
        known version prior to the commit, as well as the distance from that version
        to the commit in the git repo. Those values are used to compare Version objects.
        """
        dest = os.path.join(spack.paths.user_repos_cache_path, self.repository_uri)
        if dest.endswith(".git"):
            dest = dest[:-4]

        # prepare a cache for the repository
        dest_parent = os.path.dirname(dest)
        if not os.path.exists(dest_parent):
            mkdirp(dest_parent)

        # Only clone if we don't have it!
        if not os.path.exists(dest):
            self.fetcher.clone(dest, bare=True)

        # Lookup commit info
        with working_dir(dest):
            # TODO: we need to update the local tags if they changed on the
            # remote instance, simply adding '-f' may not be sufficient
            # (if commits are deleted on the remote, this command alone
            # won't properly update the local rev-list)
            self.fetcher.git("fetch", "--tags", output=os.devnull, error=os.devnull)

            # Ensure ref is a commit object known to git
            # Note the brackets are literals, the ref replaces the format string
            try:
                self.fetcher.git(
                    "cat-file", "-e", "%s^{commit}" % ref, output=os.devnull, error=os.devnull
                )
            except spack.util.executable.ProcessError:
                raise VersionLookupError("%s is not a valid git ref for %s" % (ref, self.pkg_name))

            # List tags (refs) by date, so last reference of a tag is newest
            tag_info = self.fetcher.git(
                "for-each-ref",
                "--sort=creatordate",
                "--format",
                "%(objectname) %(refname)",
                "refs/tags",
                output=str,
            ).split("\n")

            # Lookup of commits to spack versions
            commit_to_version = {}

            for entry in tag_info:
                if not entry:
                    continue
                tag_commit, tag = entry.split()
                tag = tag.replace("refs/tags/", "", 1)

                # For each tag, try to match to a version
                for v in [v.string for v in self.pkg.versions]:
                    if v == tag or "v" + v == tag:
                        commit_to_version[tag_commit] = v
                        break
                else:
                    # try to parse tag to copare versions spack does not know
                    match = SEMVER_REGEX.match(tag)
                    if match:
                        semver = match.groupdict()["semver"]
                        commit_to_version[tag_commit] = semver

            ancestor_commits = []
            for tag_commit in commit_to_version:
                self.fetcher.git("merge-base", "--is-ancestor", tag_commit, ref, ignore_errors=[1])
                if self.fetcher.git.returncode == 0:
                    distance = self.fetcher.git(
                        "rev-list", "%s..%s" % (tag_commit, ref), "--count", output=str, error=str
                    ).strip()
                    ancestor_commits.append((tag_commit, int(distance)))

            if ancestor_commits:
                # Get nearest ancestor that is a known version
                prev_version_commit, distance = min(ancestor_commits, key=lambda x: x[1])
                prev_version = commit_to_version[prev_version_commit]
            else:
                # Get list of all commits, this is in reverse order
                # We use this to get the first commit below
                ref_info = self.fetcher.git("log", "--all", "--pretty=format:%H", output=str)
                commits = [c for c in ref_info.split("\n") if c]

                # No previous version and distance from first commit
                prev_version = None
                distance = int(
                    self.fetcher.git(
                        "rev-list", "%s..%s" % (commits[-1], ref), "--count", output=str, error=str
                    ).strip()
                )

        return prev_version, distance
