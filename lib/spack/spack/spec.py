# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
Spack allows very fine-grained control over how packages are installed and
over how they are built and configured.  To make this easy, it has its own
syntax for declaring a dependence.  We call a descriptor of a particular
package configuration a "spec".

The syntax looks like this:

.. code-block:: sh

    $ spack install mpileaks ^openmpi @1.2:1.4 +debug %intel @12.1 target=zen
                    0        1        2        3      4      5     6

The first part of this is the command, 'spack install'.  The rest of the
line is a spec for a particular installation of the mpileaks package.

0. The package to install

1. A dependency of the package, prefixed by ^

2. A version descriptor for the package.  This can either be a specific
   version, like "1.2", or it can be a range of versions, e.g. "1.2:1.4".
   If multiple specific versions or multiple ranges are acceptable, they
   can be separated by commas, e.g. if a package will only build with
   versions 1.0, 1.2-1.4, and 1.6-1.8 of mavpich, you could say:

       depends_on("mvapich@1.0,1.2:1.4,1.6:1.8")

3. A compile-time variant of the package.  If you need openmpi to be
   built in debug mode for your package to work, you can require it by
   adding +debug to the openmpi spec when you depend on it.  If you do
   NOT want the debug option to be enabled, then replace this with -debug.
   If you would like for the variant to be propagated through all your
   package's dependencies use "++" for enabling and "--" or "~~" for disabling.

4. The name of the compiler to build with.

5. The versions of the compiler to build with.  Note that the identifier
   for a compiler version is the same '@' that is used for a package version.
   A version list denoted by '@' is associated with the compiler only if
   if it comes immediately after the compiler name.  Otherwise it will be
   associated with the current package spec.

6. The architecture to build with.  This is needed on machines where
   cross-compilation is required
"""
import collections
import collections.abc
import enum
import itertools
import os
import pathlib
import platform
import re
import socket
import warnings
from typing import Any, Callable, Dict, List, Match, Optional, Set, Tuple, Union

import llnl.path
import llnl.string
import llnl.util.filesystem as fs
import llnl.util.lang as lang
import llnl.util.tty as tty
import llnl.util.tty.color as clr

import spack.compiler
import spack.compilers
import spack.config
import spack.dependency as dp
import spack.deptypes as dt
import spack.error
import spack.hash_types as ht
import spack.parser
import spack.patch
import spack.paths
import spack.platforms
import spack.provider_index
import spack.repo
import spack.solver
import spack.store
import spack.target
import spack.traverse as traverse
import spack.util.crypto
import spack.util.executable
import spack.util.hash
import spack.util.module_cmd as md
import spack.util.prefix
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.variant as vt
import spack.version as vn
import spack.version.git_ref_lookup

__all__ = [
    "CompilerSpec",
    "Spec",
    "SpecParseError",
    "ArchitecturePropagationError",
    "DuplicateDependencyError",
    "DuplicateCompilerSpecError",
    "UnsupportedCompilerError",
    "DuplicateArchitectureError",
    "InconsistentSpecError",
    "InvalidDependencyError",
    "NoProviderError",
    "MultipleProviderError",
    "UnsatisfiableSpecNameError",
    "UnsatisfiableVersionSpecError",
    "UnsatisfiableCompilerSpecError",
    "UnsatisfiableCompilerFlagSpecError",
    "UnsatisfiableArchitectureSpecError",
    "UnsatisfiableProviderSpecError",
    "UnsatisfiableDependencySpecError",
    "AmbiguousHashError",
    "InvalidHashError",
    "SpecDeprecatedError",
]


SPEC_FORMAT_RE = re.compile(
    r"(?:"  # this is one big or, with matches ordered by priority
    # OPTION 1: escaped character (needs to be first to catch opening \{)
    # Note that an unterminated \ at the end of a string is left untouched
    r"(?:\\(.))"
    r"|"  # or
    # OPTION 2: an actual format string
    r"{"  # non-escaped open brace {
    r"([%@/]|arch=)?"  # optional sigil (to print sigil in color)
    r"(?:\^([^}\.]+)\.)?"  # optional ^depname. (to get attr from dependency)
    # after the sigil or depname, we can have a hash expression or another attribute
    r"(?:"  # one of
    r"(hash\b)(?:\:(\d+))?"  # hash followed by :<optional length>
    r"|"  # or
    r"([^}]*)"  # another attribute to format
    r")"  # end one of
    r"(})?"  # finish format string with non-escaped close brace }, or missing if not present
    r"|"
    # OPTION 3: mismatched close brace (option 2 would consume a matched open brace)
    r"(})"  # brace
    r")",
    re.IGNORECASE,
)

#: Valid pattern for an identifier in Spack

IDENTIFIER_RE = r"\w[\w-]*"

# Coloring of specs when using color output. Fields are printed with
# different colors to enhance readability.
# See llnl.util.tty.color for descriptions of the color codes.
COMPILER_COLOR = "@g"  #: color for highlighting compilers
VERSION_COLOR = "@c"  #: color for highlighting versions
ARCHITECTURE_COLOR = "@m"  #: color for highlighting architectures
VARIANT_COLOR = "@B"  #: color for highlighting variants
HASH_COLOR = "@K"  #: color for highlighting package hashes

#: Default format for Spec.format(). This format can be round-tripped, so that:
#:     Spec(Spec("string").format()) == Spec("string)"
DEFAULT_FORMAT = (
    "{name}{@versions}"
    "{%compiler.name}{@compiler.versions}{compiler_flags}"
    "{variants}{arch=architecture}{/abstract_hash}"
)

#: Display format, which eliminates extra `@=` in the output, for readability.
DISPLAY_FORMAT = (
    "{name}{@version}"
    "{%compiler.name}{@compiler.version}{compiler_flags}"
    "{variants}{arch=architecture}{/abstract_hash}"
)

#: Regular expression to pull spec contents out of clearsigned signature
#: file.
CLEARSIGN_FILE_REGEX = re.compile(
    (
        r"^-----BEGIN PGP SIGNED MESSAGE-----"
        r"\s+Hash:\s+[^\s]+\s+(.+)-----BEGIN PGP SIGNATURE-----"
    ),
    re.MULTILINE | re.DOTALL,
)

#: specfile format version. Must increase monotonically
SPECFILE_FORMAT_VERSION = 4


class InstallStatus(enum.Enum):
    """Maps install statuses to symbols for display.

    Options are artificially disjoint for display purposes
    """

    installed = "@g{[+]}  "
    upstream = "@g{[^]}  "
    external = "@g{[e]}  "
    absent = "@K{ - }  "
    missing = "@r{[-]}  "


# regexes used in spec formatting
OLD_STYLE_FMT_RE = re.compile(r"\${[A-Z]+}")


def ensure_modern_format_string(fmt: str) -> None:
    """Ensure that the format string does not contain old ${...} syntax."""
    result = OLD_STYLE_FMT_RE.search(fmt)
    if result:
        raise SpecFormatStringError(
            f"Format string `{fmt}` contains old syntax `{result.group(0)}`. "
            "This is no longer supported."
        )


@lang.lazy_lexicographic_ordering
class ArchSpec:
    """Aggregate the target platform, the operating system and the target microarchitecture."""

    @staticmethod
    def _return_arch(os_tag, target_tag):
        platform = spack.platforms.host()
        default_os = platform.operating_system(os_tag)
        default_target = platform.target(target_tag)
        arch_tuple = str(platform), str(default_os), str(default_target)
        return ArchSpec(arch_tuple)

    @staticmethod
    def default_arch():
        """Return the default architecture"""
        return ArchSpec._return_arch("default_os", "default_target")

    @staticmethod
    def frontend_arch():
        """Return the frontend architecture"""
        return ArchSpec._return_arch("frontend", "frontend")

    __slots__ = "_platform", "_os", "_target"

    def __init__(self, spec_or_platform_tuple=(None, None, None)):
        """Architecture specification a package should be built with.

        Each ArchSpec is comprised of three elements: a platform (e.g. Linux),
        an OS (e.g. RHEL6), and a target (e.g. x86_64).

        Args:
            spec_or_platform_tuple (ArchSpec or str or tuple): if an ArchSpec
                is passed it will be duplicated into the new instance.
                Otherwise information on platform, OS and target should be
                passed in either as a spec string or as a tuple.
        """

        # If the argument to __init__ is a spec string, parse it
        # and construct an ArchSpec
        def _string_or_none(s):
            if s and s != "None":
                return str(s)
            return None

        # If another instance of ArchSpec was passed, duplicate it
        if isinstance(spec_or_platform_tuple, ArchSpec):
            other = spec_or_platform_tuple
            platform_tuple = other.platform, other.os, other.target

        elif isinstance(spec_or_platform_tuple, (str, tuple)):
            spec_fields = spec_or_platform_tuple

            # Normalize the string to a tuple
            if isinstance(spec_or_platform_tuple, str):
                spec_fields = spec_or_platform_tuple.split("-")
                if len(spec_fields) != 3:
                    msg = "cannot construct an ArchSpec from {0!s}"
                    raise ValueError(msg.format(spec_or_platform_tuple))

            platform, operating_system, target = spec_fields
            platform_tuple = (_string_or_none(platform), _string_or_none(operating_system), target)

        self.platform, self.os, self.target = platform_tuple

    @staticmethod
    def override(init_spec, change_spec):
        if init_spec:
            new_spec = init_spec.copy()
        else:
            new_spec = ArchSpec()
        if change_spec.platform:
            new_spec.platform = change_spec.platform
            # TODO: if the platform is changed to something that is incompatible
            # with the current os, we should implicitly remove it
        if change_spec.os:
            new_spec.os = change_spec.os
        if change_spec.target:
            new_spec.target = change_spec.target
        return new_spec

    def _autospec(self, spec_like):
        if isinstance(spec_like, ArchSpec):
            return spec_like
        return ArchSpec(spec_like)

    def _cmp_iter(self):
        yield self.platform
        yield self.os
        yield self.target

    @property
    def platform(self):
        """The platform of the architecture."""
        return self._platform

    @platform.setter
    def platform(self, value):
        # The platform of the architecture spec will be verified as a
        # supported Spack platform before it's set to ensure all specs
        # refer to valid platforms.
        value = str(value) if value is not None else None
        self._platform = value

    @property
    def os(self):
        """The OS of this ArchSpec."""
        return self._os

    @os.setter
    def os(self, value):
        # The OS of the architecture spec will update the platform field
        # if the OS is set to one of the reserved OS types so that the
        # default OS type can be resolved.  Since the reserved OS
        # information is only available for the host machine, the platform
        # will assumed to be the host machine's platform.
        value = str(value) if value is not None else None

        if value in spack.platforms.Platform.reserved_oss:
            curr_platform = str(spack.platforms.host())
            self.platform = self.platform or curr_platform

            if self.platform != curr_platform:
                raise ValueError(
                    "Can't set arch spec OS to reserved value '%s' when the "
                    "arch platform (%s) isn't the current platform (%s)"
                    % (value, self.platform, curr_platform)
                )

            spec_platform = spack.platforms.by_name(self.platform)
            value = str(spec_platform.operating_system(value))

        self._os = value

    @property
    def target(self):
        """The target of the architecture."""
        return self._target

    @target.setter
    def target(self, value):
        # The target of the architecture spec will update the platform field
        # if the target is set to one of the reserved target types so that
        # the default target type can be resolved.  Since the reserved target
        # information is only available for the host machine, the platform
        # will assumed to be the host machine's platform.

        def target_or_none(t):
            if isinstance(t, spack.target.Target):
                return t
            if t and t != "None":
                return spack.target.Target(t)
            return None

        value = target_or_none(value)

        if str(value) in spack.platforms.Platform.reserved_targets:
            curr_platform = str(spack.platforms.host())
            self.platform = self.platform or curr_platform

            if self.platform != curr_platform:
                raise ValueError(
                    "Can't set arch spec target to reserved value '%s' when "
                    "the arch platform (%s) isn't the current platform (%s)"
                    % (value, self.platform, curr_platform)
                )

            spec_platform = spack.platforms.by_name(self.platform)
            value = spec_platform.target(value)

        self._target = value

    def satisfies(self, other: "ArchSpec") -> bool:
        """Return True if all concrete specs matching self also match other, otherwise False.

        Args:
            other: spec to be satisfied
        """
        other = self._autospec(other)

        # Check platform and os
        for attribute in ("platform", "os"):
            other_attribute = getattr(other, attribute)
            self_attribute = getattr(self, attribute)
            if other_attribute and self_attribute != other_attribute:
                return False

        return self._target_satisfies(other, strict=True)

    def intersects(self, other: "ArchSpec") -> bool:
        """Return True if there exists at least one concrete spec that matches both
        self and other, otherwise False.

        This operation is commutative, and if two specs intersect it means that one
        can constrain the other.

        Args:
            other: spec to be checked for compatibility
        """
        other = self._autospec(other)

        # Check platform and os
        for attribute in ("platform", "os"):
            other_attribute = getattr(other, attribute)
            self_attribute = getattr(self, attribute)
            if other_attribute and self_attribute and self_attribute != other_attribute:
                return False

        return self._target_satisfies(other, strict=False)

    def _target_satisfies(self, other: "ArchSpec", strict: bool) -> bool:
        if strict is True:
            need_to_check = bool(other.target)
        else:
            need_to_check = bool(other.target and self.target)

        if not need_to_check:
            return True

        # other_target is there and strict=True
        if self.target is None:
            return False

        return bool(self._target_intersection(other))

    def _target_constrain(self, other: "ArchSpec") -> bool:
        if not other._target_satisfies(self, strict=False):
            raise UnsatisfiableArchitectureSpecError(self, other)

        if self.target_concrete:
            return False

        elif other.target_concrete:
            self.target = other.target
            return True

        # Compute the intersection of every combination of ranges in the lists
        results = self._target_intersection(other)
        attribute_str = ",".join(results)

        if self.target == attribute_str:
            return False

        self.target = attribute_str
        return True

    def _target_intersection(self, other):
        results = []

        if not self.target or not other.target:
            return results

        for s_target_range in str(self.target).split(","):
            s_min, s_sep, s_max = s_target_range.partition(":")
            for o_target_range in str(other.target).split(","):
                o_min, o_sep, o_max = o_target_range.partition(":")

                if not s_sep:
                    # s_target_range is a concrete target
                    # get a microarchitecture reference for at least one side
                    # of each comparison so we can use archspec comparators
                    s_comp = spack.target.Target(s_min).microarchitecture
                    if not o_sep:
                        if s_min == o_min:
                            results.append(s_min)
                    elif (not o_min or s_comp >= o_min) and (not o_max or s_comp <= o_max):
                        results.append(s_min)
                elif not o_sep:
                    # "cast" to microarchitecture
                    o_comp = spack.target.Target(o_min).microarchitecture
                    if (not s_min or o_comp >= s_min) and (not s_max or o_comp <= s_max):
                        results.append(o_min)
                else:
                    # Take intersection of two ranges
                    # Lots of comparisons needed
                    _s_min = spack.target.Target(s_min).microarchitecture
                    _s_max = spack.target.Target(s_max).microarchitecture
                    _o_min = spack.target.Target(o_min).microarchitecture
                    _o_max = spack.target.Target(o_max).microarchitecture

                    n_min = s_min if _s_min >= _o_min else o_min
                    n_max = s_max if _s_max <= _o_max else o_max
                    _n_min = spack.target.Target(n_min).microarchitecture
                    _n_max = spack.target.Target(n_max).microarchitecture
                    if _n_min == _n_max:
                        results.append(n_min)
                    elif not n_min or not n_max or _n_min < _n_max:
                        results.append("%s:%s" % (n_min, n_max))
        return results

    def constrain(self, other: "ArchSpec") -> bool:
        """Projects all architecture fields that are specified in the given
        spec onto the instance spec if they're missing from the instance
        spec.

        This will only work if the two specs are compatible.

        Args:
            other (ArchSpec or str): constraints to be added

        Returns:
            True if the current instance was constrained, False otherwise.
        """
        other = self._autospec(other)

        if not other.intersects(self):
            raise UnsatisfiableArchitectureSpecError(other, self)

        constrained = False
        for attr in ("platform", "os"):
            svalue, ovalue = getattr(self, attr), getattr(other, attr)
            if svalue is None and ovalue is not None:
                setattr(self, attr, ovalue)
                constrained = True

        constrained |= self._target_constrain(other)

        return constrained

    def copy(self):
        """Copy the current instance and returns the clone."""
        return ArchSpec(self)

    @property
    def concrete(self):
        """True if the spec is concrete, False otherwise"""
        return self.platform and self.os and self.target and self.target_concrete

    @property
    def target_concrete(self):
        """True if the target is not a range or list."""
        return (
            self.target is not None and ":" not in str(self.target) and "," not in str(self.target)
        )

    def to_dict(self):
        d = syaml.syaml_dict(
            [
                ("platform", self.platform),
                ("platform_os", self.os),
                ("target", self.target.to_dict_or_value()),
            ]
        )
        return syaml.syaml_dict([("arch", d)])

    @staticmethod
    def from_dict(d):
        """Import an ArchSpec from raw YAML/JSON data"""
        arch = d["arch"]
        target = spack.target.Target.from_dict_or_value(arch["target"])
        return ArchSpec((arch["platform"], arch["platform_os"], target))

    def __str__(self):
        return "%s-%s-%s" % (self.platform, self.os, self.target)

    def __repr__(self):
        fmt = "ArchSpec(({0.platform!r}, {0.os!r}, {1!r}))"
        return fmt.format(self, str(self.target))

    def __contains__(self, string):
        return string in str(self) or string in self.target


@lang.lazy_lexicographic_ordering
class CompilerSpec:
    """The CompilerSpec field represents the compiler or range of compiler
    versions that a package should be built with.  CompilerSpecs have a
    name and a version list."""

    __slots__ = "name", "versions"

    def __init__(self, *args):
        nargs = len(args)
        if nargs == 1:
            arg = args[0]
            # If there is one argument, it's either another CompilerSpec
            # to copy or a string to parse
            if isinstance(arg, str):
                spec = spack.parser.parse_one_or_raise(f"%{arg}")
                self.name = spec.compiler.name
                self.versions = spec.compiler.versions

            elif isinstance(arg, CompilerSpec):
                self.name = arg.name
                self.versions = arg.versions.copy()

            else:
                raise TypeError(
                    "Can only build CompilerSpec from string or "
                    + "CompilerSpec. Found %s" % type(arg)
                )

        elif nargs == 2:
            name, version = args
            self.name = name
            self.versions = vn.VersionList([vn.ver(version)])

        else:
            raise TypeError("__init__ takes 1 or 2 arguments. (%d given)" % nargs)

    def _autospec(self, compiler_spec_like):
        if isinstance(compiler_spec_like, CompilerSpec):
            return compiler_spec_like
        return CompilerSpec(compiler_spec_like)

    def intersects(self, other: "CompilerSpec") -> bool:
        """Return True if all concrete specs matching self also match other, otherwise False.

        For compiler specs this means that the name of the compiler must be the same for
        self and other, and that the versions ranges should intersect.

        Args:
            other: spec to be satisfied
        """
        other = self._autospec(other)
        return self.name == other.name and self.versions.intersects(other.versions)

    def satisfies(self, other: "CompilerSpec") -> bool:
        """Return True if all concrete specs matching self also match other, otherwise False.

        For compiler specs this means that the name of the compiler must be the same for
        self and other, and that the version range of self is a subset of that of other.

        Args:
            other: spec to be satisfied
        """
        other = self._autospec(other)
        return self.name == other.name and self.versions.satisfies(other.versions)

    def constrain(self, other: "CompilerSpec") -> bool:
        """Intersect self's versions with other.

        Return whether the CompilerSpec changed.
        """
        other = self._autospec(other)

        # ensure that other will actually constrain this spec.
        if not other.intersects(self):
            raise UnsatisfiableCompilerSpecError(other, self)

        return self.versions.intersect(other.versions)

    @property
    def concrete(self):
        """A CompilerSpec is concrete if its versions are concrete and there
        is an available compiler with the right version."""
        return self.versions.concrete

    @property
    def version(self):
        if not self.concrete:
            raise spack.error.SpecError("Spec is not concrete: " + str(self))
        return self.versions[0]

    def copy(self):
        clone = CompilerSpec.__new__(CompilerSpec)
        clone.name = self.name
        clone.versions = self.versions.copy()
        return clone

    def _cmp_iter(self):
        yield self.name
        yield self.versions

    def to_dict(self):
        d = syaml.syaml_dict([("name", self.name)])
        d.update(self.versions.to_dict())

        return syaml.syaml_dict([("compiler", d)])

    @staticmethod
    def from_dict(d):
        d = d["compiler"]
        return CompilerSpec(d["name"], vn.VersionList.from_dict(d))

    @property
    def display_str(self):
        """Equivalent to {compiler.name}{@compiler.version} for Specs, without extra
        @= for readability."""
        if self.concrete:
            return f"{self.name}@{self.version}"
        elif self.versions != vn.any_version:
            return f"{self.name}@{self.versions}"
        return self.name

    def __str__(self):
        out = self.name
        if self.versions and self.versions != vn.any_version:
            out += f"@{self.versions}"
        return out

    def __repr__(self):
        return str(self)


@lang.lazy_lexicographic_ordering
class DependencySpec:
    """DependencySpecs represent an edge in the DAG, and contain dependency types
    and information on the virtuals being provided.

    Dependencies can be one (or more) of several types:

    - build: needs to be in the PATH at build time.
    - link: is linked to and added to compiler flags.
    - run: needs to be in the PATH for the package to run.

    Args:
        parent: starting node of the edge
        spec: ending node of the edge.
        depflag: represents dependency relationships.
        virtuals: virtual packages provided from child to parent node.
    """

    __slots__ = "parent", "spec", "depflag", "virtuals"

    def __init__(
        self, parent: "Spec", spec: "Spec", *, depflag: dt.DepFlag, virtuals: Tuple[str, ...]
    ):
        self.parent = parent
        self.spec = spec
        self.depflag = depflag
        self.virtuals = tuple(sorted(set(virtuals)))

    def update_deptypes(self, depflag: dt.DepFlag) -> bool:
        """Update the current dependency types"""
        old = self.depflag
        new = depflag | old
        if new == old:
            return False
        self.depflag = new
        return True

    def update_virtuals(self, virtuals: Tuple[str, ...]) -> bool:
        """Update the list of provided virtuals"""
        old = self.virtuals
        self.virtuals = tuple(sorted(set(virtuals).union(self.virtuals)))
        return old != self.virtuals

    def copy(self) -> "DependencySpec":
        """Return a copy of this edge"""
        return DependencySpec(self.parent, self.spec, depflag=self.depflag, virtuals=self.virtuals)

    def _cmp_iter(self):
        yield self.parent.name if self.parent else None
        yield self.spec.name if self.spec else None
        yield self.depflag
        yield self.virtuals

    def __str__(self) -> str:
        parent = self.parent.name if self.parent else None
        child = self.spec.name if self.spec else None
        return f"{parent} {self.depflag}[virtuals={','.join(self.virtuals)}] --> {child}"

    def flip(self) -> "DependencySpec":
        """Flip the dependency, and drop virtual information"""
        return DependencySpec(
            parent=self.spec, spec=self.parent, depflag=self.depflag, virtuals=()
        )


class CompilerFlag(str):
    """Will store a flag value and it's propagation value

    Args:
        value (str): the flag's value
        propagate (bool): if ``True`` the flag value will
            be passed to the package's dependencies. If
            ``False`` it will not
    """

    def __new__(cls, value, **kwargs):
        obj = str.__new__(cls, value)
        obj.propagate = kwargs.pop("propagate", False)
        return obj


_valid_compiler_flags = ["cflags", "cxxflags", "fflags", "ldflags", "ldlibs", "cppflags"]


class FlagMap(lang.HashableMap):
    __slots__ = ("spec",)

    def __init__(self, spec):
        super().__init__()
        self.spec = spec

    def satisfies(self, other):
        return all(f in self and self[f] == other[f] for f in other)

    def intersects(self, other):
        common_types = set(self) & set(other)
        for flag_type in common_types:
            if not self[flag_type] or not other[flag_type]:
                # At least one of the two is empty
                continue

            if self[flag_type] != other[flag_type]:
                return False

            if not all(
                f1.propagate == f2.propagate for f1, f2 in zip(self[flag_type], other[flag_type])
            ):
                # At least one propagation flag didn't match
                return False
        return True

    def constrain(self, other):
        """Add all flags in other that aren't in self to self.

        Return whether the spec changed.
        """
        if other.spec and other.spec._concrete:
            for k in self:
                if k not in other:
                    raise UnsatisfiableCompilerFlagSpecError(self[k], "<absent>")

        changed = False
        for k in other:
            if k in self and not set(self[k]) <= set(other[k]):
                raise UnsatisfiableCompilerFlagSpecError(
                    " ".join(f for f in self[k]), " ".join(f for f in other[k])
                )
            elif k not in self:
                self[k] = other[k]
                changed = True

            # Check that the propagation values match
            if self[k] == other[k]:
                for i in range(len(other[k])):
                    if self[k][i].propagate != other[k][i].propagate:
                        raise UnsatisfiableCompilerFlagSpecError(
                            self[k][i].propagate, other[k][i].propagate
                        )
        return changed

    @staticmethod
    def valid_compiler_flags():
        return _valid_compiler_flags

    def copy(self):
        clone = FlagMap(self.spec)
        for name, compiler_flag in self.items():
            clone[name] = compiler_flag
        return clone

    def add_flag(self, flag_type, value, propagation):
        """Stores the flag's value in CompilerFlag and adds it
        to the FlagMap

        Args:
            flag_type (str): the type of flag
            value (str): the flag's value that will be added to the flag_type's
                corresponding list
            propagation (bool): if ``True`` the flag value will be passed to
                the packages' dependencies. If``False`` it will not be passed
        """
        flag = CompilerFlag(value, propagate=propagation)

        if flag_type not in self:
            self[flag_type] = [flag]
        else:
            self[flag_type].append(flag)

    def yaml_entry(self, flag_type):
        """Returns the flag type and a list of the flag values since the
        propagation values aren't needed when writing to yaml

        Args:
            flag_type (str): the type of flag to get values from

        Returns the flag_type and a list of the corresponding flags in
            string format
        """
        return flag_type, [str(flag) for flag in self[flag_type]]

    def _cmp_iter(self):
        for k, v in sorted(self.items()):
            yield k

            def flags():
                for flag in v:
                    yield flag

            yield flags

    def __str__(self):
        if not self:
            return ""

        sorted_items = sorted((k, v) for k, v in self.items() if v)

        result = ""
        for flag_type, flags in sorted_items:
            normal = [f for f in flags if not f.propagate]
            if normal:
                result += f" {flag_type}={spack.parser.quote_if_needed(' '.join(normal))}"

            propagated = [f for f in flags if f.propagate]
            if propagated:
                result += f" {flag_type}=={spack.parser.quote_if_needed(' '.join(propagated))}"

        # TODO: somehow add this space only if something follows in Spec.format()
        if sorted_items:
            result += " "

        return result


def _sort_by_dep_types(dspec: DependencySpec):
    return dspec.depflag


#: Enum for edge directions
EdgeDirection = lang.enum(parent=0, child=1)


@lang.lazy_lexicographic_ordering
class _EdgeMap(collections.abc.Mapping):
    """Represent a collection of edges (DependencySpec objects) in the DAG.

    Objects of this class are used in Specs to track edges that are
    outgoing towards direct dependencies, or edges that are incoming
    from direct dependents.

    Edges are stored in a dictionary and keyed by package name.
    """

    __slots__ = "edges", "store_by_child"

    def __init__(self, store_by=EdgeDirection.child):
        # Sanitize input arguments
        msg = 'unexpected value for "store_by" argument'
        assert store_by in (EdgeDirection.child, EdgeDirection.parent), msg

        #: This dictionary maps a package name to a list of edges
        #: i.e. to a list of DependencySpec objects
        self.edges = {}
        self.store_by_child = store_by == EdgeDirection.child

    def __getitem__(self, key):
        return self.edges[key]

    def __iter__(self):
        return iter(self.edges)

    def __len__(self):
        return len(self.edges)

    def add(self, edge: DependencySpec):
        key = edge.spec.name if self.store_by_child else edge.parent.name
        if key in self.edges:
            lst = self.edges[key]
            lst.append(edge)
            lst.sort(key=_sort_by_dep_types)
        else:
            self.edges[key] = [edge]

    def __str__(self):
        return "{deps: %s}" % ", ".join(str(d) for d in sorted(self.values()))

    def _cmp_iter(self):
        for item in sorted(itertools.chain.from_iterable(self.edges.values())):
            yield item

    def copy(self):
        """Copies this object and returns a clone"""
        clone = type(self)()
        clone.store_by_child = self.store_by_child

        # Copy everything from this dict into it.
        for dspec in itertools.chain.from_iterable(self.values()):
            clone.add(dspec.copy())

        return clone

    def select(self, parent=None, child=None, depflag: dt.DepFlag = dt.ALL):
        """Select a list of edges and return them.

        If an edge:
        - Has *any* of the dependency types passed as argument,
        - Matches the parent and/or child name, if passed
        then it is selected.

        The deptypes argument needs to be a flag, since the method won't
        convert it for performance reason.

        Args:
            parent (str): name of the parent package
            child (str): name of the child package
            depflag: allowed dependency types in flag form

        Returns:
            List of DependencySpec objects
        """
        if not depflag:
            return []

        # Start from all the edges we store
        selected = (d for d in itertools.chain.from_iterable(self.values()))

        # Filter by parent name
        if parent:
            selected = (d for d in selected if d.parent.name == parent)

        # Filter by child name
        if child:
            selected = (d for d in selected if d.spec.name == child)

        # Filter by allowed dependency types
        selected = (dep for dep in selected if not dep.depflag or (depflag & dep.depflag))

        return list(selected)

    def clear(self):
        self.edges.clear()


def _command_default_handler(spec: "Spec"):
    """Default handler when looking for the 'command' attribute.

    Tries to search for ``spec.name`` in the ``spec.home.bin`` directory.

    Parameters:
        spec: spec that is being queried

    Returns:
        Executable: An executable of the command

    Raises:
        RuntimeError: If the command is not found
    """
    home = getattr(spec.package, "home")
    path = os.path.join(home.bin, spec.name)

    if fs.is_exe(path):
        return spack.util.executable.Executable(path)
    raise RuntimeError(f"Unable to locate {spec.name} command in {home.bin}")


def _headers_default_handler(spec: "Spec"):
    """Default handler when looking for the 'headers' attribute.

    Tries to search for ``*.h`` files recursively starting from
    ``spec.package.home.include``.

    Parameters:
        spec: spec that is being queried

    Returns:
        HeaderList: The headers in ``prefix.include``

    Raises:
        NoHeadersError: If no headers are found
    """
    home = getattr(spec.package, "home")
    headers = fs.find_headers("*", root=home.include, recursive=True)

    if headers:
        return headers
    raise spack.error.NoHeadersError(f"Unable to locate {spec.name} headers in {home}")


def _libs_default_handler(spec: "Spec"):
    """Default handler when looking for the 'libs' attribute.

    Tries to search for ``lib{spec.name}`` recursively starting from
    ``spec.package.home``. If ``spec.name`` starts with ``lib``, searches for
    ``{spec.name}`` instead.

    Parameters:
        spec: spec that is being queried

    Returns:
        LibraryList: The libraries found

    Raises:
        NoLibrariesError: If no libraries are found
    """

    # Variable 'name' is passed to function 'find_libraries', which supports
    # glob characters. For example, we have a package with a name 'abc-abc'.
    # Now, we don't know if the original name of the package is 'abc_abc'
    # (and it generates a library 'libabc_abc.so') or 'abc-abc' (and it
    # generates a library 'libabc-abc.so'). So, we tell the function
    # 'find_libraries' to give us anything that matches 'libabc?abc' and it
    # gives us either 'libabc-abc.so' or 'libabc_abc.so' (or an error)
    # depending on which one exists (there is a possibility, of course, to
    # get something like 'libabcXabc.so, but for now we consider this
    # unlikely).
    name = spec.name.replace("-", "?")
    home = getattr(spec.package, "home")

    # Avoid double 'lib' for packages whose names already start with lib
    if not name.startswith("lib") and not spec.satisfies("platform=windows"):
        name = "lib" + name

    # If '+shared' search only for shared library; if '~shared' search only for
    # static library; otherwise, first search for shared and then for static.
    search_shared = (
        [True] if ("+shared" in spec) else ([False] if ("~shared" in spec) else [True, False])
    )

    for shared in search_shared:
        # Since we are searching for link libraries, on Windows search only for
        # ".Lib" extensions by default as those represent import libraries for implict links.
        libs = fs.find_libraries(name, home, shared=shared, recursive=True, runtime=False)
        if libs:
            return libs

    raise spack.error.NoLibrariesError(
        f"Unable to recursively locate {spec.name} libraries in {home}"
    )


class ForwardQueryToPackage:
    """Descriptor used to forward queries from Spec to Package"""

    def __init__(
        self,
        attribute_name: str,
        default_handler: Optional[Callable[["Spec"], Any]] = None,
        _indirect: bool = False,
    ) -> None:
        """Create a new descriptor.

        Parameters:
            attribute_name: name of the attribute to be searched for in the Package instance
            default_handler: default function to be called if the attribute was not found in the
                Package instance
            _indirect: temporarily added to redirect a query to another package.
        """
        self.attribute_name = attribute_name
        self.default = default_handler
        self.indirect = _indirect

    def __get__(self, instance: "SpecBuildInterface", cls):
        """Retrieves the property from Package using a well defined chain
        of responsibility.

        The order of call is:

        1. if the query was through the name of a virtual package try to
            search for the attribute `{virtual_name}_{attribute_name}`
            in Package

        2. try to search for attribute `{attribute_name}` in Package

        3. try to call the default handler

        The first call that produces a value will stop the chain.

        If no call can handle the request then AttributeError is raised with a
        message indicating that no relevant attribute exists.
        If a call returns None, an AttributeError is raised with a message
        indicating a query failure, e.g. that library files were not found in a
        'libs' query.
        """
        # TODO: this indirection exist solely for `spec["python"].command` to actually return
        # spec["python-venv"].command. It should be removed when `python` is a virtual.
        if self.indirect and instance.indirect_spec:
            pkg = instance.indirect_spec.package
        else:
            pkg = instance.wrapped_obj.package
        try:
            query = instance.last_query
        except AttributeError:
            # There has been no query yet: this means
            # a spec is trying to access its own attributes
            _ = instance.wrapped_obj[instance.wrapped_obj.name]  # NOQA: ignore=F841
            query = instance.last_query

        callbacks_chain = []
        # First in the chain : specialized attribute for virtual packages
        if query.isvirtual:
            specialized_name = "{0}_{1}".format(query.name, self.attribute_name)
            callbacks_chain.append(lambda: getattr(pkg, specialized_name))
        # Try to get the generic method from Package
        callbacks_chain.append(lambda: getattr(pkg, self.attribute_name))
        # Final resort : default callback
        if self.default is not None:
            _default = self.default  # make mypy happy
            callbacks_chain.append(lambda: _default(instance.wrapped_obj))

        # Trigger the callbacks in order, the first one producing a
        # value wins
        value = None
        message = None
        for f in callbacks_chain:
            try:
                value = f()
                # A callback can return None to trigger an error indicating
                # that the query failed.
                if value is None:
                    msg = "Query of package '{name}' for '{attrib}' failed\n"
                    msg += "\tprefix : {spec.prefix}\n"
                    msg += "\tspec : {spec}\n"
                    msg += "\tqueried as : {query.name}\n"
                    msg += "\textra parameters : {query.extra_parameters}"
                    message = msg.format(
                        name=pkg.name,
                        attrib=self.attribute_name,
                        spec=instance,
                        query=instance.last_query,
                    )
                else:
                    return value
                break
            except AttributeError:
                pass
        # value is 'None'
        if message is not None:
            # Here we can use another type of exception. If we do that, the
            # unit test 'test_getitem_exceptional_paths' in the file
            # lib/spack/spack/test/spec_dag.py will need to be updated to match
            # the type.
            raise AttributeError(message)
        # 'None' value at this point means that there are no appropriate
        # properties defined and no default handler, or that all callbacks
        # raised AttributeError. In this case, we raise AttributeError with an
        # appropriate message.
        fmt = "'{name}' package has no relevant attribute '{query}'\n"
        fmt += "\tspec : '{spec}'\n"
        fmt += "\tqueried as : '{spec.last_query.name}'\n"
        fmt += "\textra parameters : '{spec.last_query.extra_parameters}'\n"
        message = fmt.format(name=pkg.name, query=self.attribute_name, spec=instance)
        raise AttributeError(message)

    def __set__(self, instance, value):
        cls_name = type(instance).__name__
        msg = "'{0}' object attribute '{1}' is read-only"
        raise AttributeError(msg.format(cls_name, self.attribute_name))


# Represents a query state in a BuildInterface object
QueryState = collections.namedtuple("QueryState", ["name", "extra_parameters", "isvirtual"])


class SpecBuildInterface(lang.ObjectWrapper):
    # home is available in the base Package so no default is needed
    home = ForwardQueryToPackage("home", default_handler=None)
    headers = ForwardQueryToPackage("headers", default_handler=_headers_default_handler)
    libs = ForwardQueryToPackage("libs", default_handler=_libs_default_handler)
    command = ForwardQueryToPackage(
        "command", default_handler=_command_default_handler, _indirect=True
    )

    def __init__(self, spec: "Spec", name: str, query_parameters: List[str], _parent: "Spec"):
        super().__init__(spec)
        # Adding new attributes goes after super() call since the ObjectWrapper
        # resets __dict__ to behave like the passed object
        original_spec = getattr(spec, "wrapped_obj", spec)
        self.wrapped_obj = original_spec
        self.token = original_spec, name, query_parameters, _parent
        is_virtual = spack.repo.PATH.is_virtual(name)
        self.last_query = QueryState(
            name=name, extra_parameters=query_parameters, isvirtual=is_virtual
        )

        # TODO: this ad-hoc logic makes `spec["python"].command` return
        # `spec["python-venv"].command` and should be removed when `python` is a virtual.
        self.indirect_spec = None
        if spec.name == "python":
            python_venvs = _parent.dependencies("python-venv")
            if not python_venvs:
                return
            self.indirect_spec = python_venvs[0]

    def __reduce__(self):
        return SpecBuildInterface, self.token

    def copy(self, *args, **kwargs):
        return self.wrapped_obj.copy(*args, **kwargs)


@lang.lazy_lexicographic_ordering(set_hash=False)
class Spec:
    #: Cache for spec's prefix, computed lazily in the corresponding property
    _prefix = None
    abstract_hash = None

    @staticmethod
    def default_arch():
        """Return an anonymous spec for the default architecture"""
        s = Spec()
        s.architecture = ArchSpec.default_arch()
        return s

    def __init__(
        self,
        spec_like=None,
        normal=False,
        concrete=False,
        external_path=None,
        external_modules=None,
    ):
        """Create a new Spec.

        Arguments:
            spec_like (optional string): if not provided, we initialize
                an anonymous Spec that matches any Spec object; if
                provided we parse this as a Spec string.

        Keyword arguments:
        # assign special fields from constructor
        self._normal = normal
        self._concrete = concrete
        self.external_path = external_path
        self.external_module = external_module
        """
        # Copy if spec_like is a Spec.
        if isinstance(spec_like, Spec):
            self._dup(spec_like)
            return

        # init an empty spec that matches anything.
        self.name = None
        self.versions = vn.VersionList(":")
        self.variants = vt.VariantMap(self)
        self.architecture = None
        self.compiler = None
        self.compiler_flags = FlagMap(self)
        self._dependents = _EdgeMap(store_by=EdgeDirection.parent)
        self._dependencies = _EdgeMap(store_by=EdgeDirection.child)
        self.namespace = None

        # initial values for all spec hash types
        for h in ht.hashes:
            setattr(self, h.attr, None)

        # Python __hash__ is handled separately from the cached spec hashes
        self._dunder_hash = None

        # cache of package for this spec
        self._package = None

        # Most of these are internal implementation details that can be
        # set by internal Spack calls in the constructor.
        #
        # For example, Specs are by default not assumed to be normal, but
        # in some cases we've read them from a file want to assume
        # normal.  This allows us to manipulate specs that Spack doesn't
        # have package.py files for.
        self._normal = normal
        self._concrete = concrete
        self._external_path = external_path
        self.external_modules = Spec._format_module_list(external_modules)

        # This attribute is used to store custom information for
        # external specs. None signal that it was not set yet.
        self.extra_attributes = None

        # This attribute holds the original build copy of the spec if it is
        # deployed differently than it was built. None signals that the spec
        # is deployed "as built."
        # Build spec should be the actual build spec unless marked dirty.
        self._build_spec = None

        if isinstance(spec_like, str):
            spack.parser.parse_one_or_raise(spec_like, self)

        elif spec_like is not None:
            raise TypeError("Can't make spec out of %s" % type(spec_like))

    @staticmethod
    def _format_module_list(modules):
        """Return a module list that is suitable for YAML serialization
        and hash computation.

        Given a module list, possibly read from a configuration file,
        return an object that serializes to a consistent YAML string
        before/after round-trip serialization to/from a Spec dictionary
        (stored in JSON format): when read in, the module list may
        contain YAML formatting that is discarded (non-essential)
        when stored as a Spec dictionary; we take care in this function
        to discard such formatting such that the Spec hash does not
        change before/after storage in JSON.
        """
        if modules:
            modules = list(modules)
        return modules

    @property
    def external_path(self):
        return llnl.path.path_to_os_path(self._external_path)[0]

    @external_path.setter
    def external_path(self, ext_path):
        self._external_path = ext_path

    @property
    def external(self):
        return bool(self.external_path) or bool(self.external_modules)

    @property
    def is_develop(self):
        """Return whether the Spec represents a user-developed package
        in a Spack ``Environment`` (i.e. using `spack develop`).
        """
        return bool(self.variants.get("dev_path", False))

    def clear_dependencies(self):
        """Trim the dependencies of this spec."""
        self._dependencies.clear()

    def clear_edges(self):
        """Trim the dependencies and dependents of this spec."""
        self._dependencies.clear()
        self._dependents.clear()

    def detach(self, deptype="all"):
        """Remove any reference that dependencies have of this node.

        Args:
            deptype (str or tuple): dependency types tracked by the
                current spec
        """
        key = self.dag_hash()
        # Go through the dependencies
        for dep in self.dependencies(deptype=deptype):
            # Remove the spec from dependents
            if self.name in dep._dependents:
                dependents_copy = dep._dependents.edges[self.name]
                del dep._dependents.edges[self.name]
                for edge in dependents_copy:
                    if edge.parent.dag_hash() == key:
                        continue
                    dep._dependents.add(edge)

    def _get_dependency(self, name):
        # WARNING: This function is an implementation detail of the
        # WARNING: original concretizer. Since with that greedy
        # WARNING: algorithm we don't allow multiple nodes from
        # WARNING: the same package in a DAG, here we hard-code
        # WARNING: using index 0 i.e. we assume that we have only
        # WARNING: one edge from package "name"
        deps = self.edges_to_dependencies(name=name)
        if len(deps) != 1:
            err_msg = 'expected only 1 "{0}" dependency, but got {1}'
            raise spack.error.SpecError(err_msg.format(name, len(deps)))
        return deps[0]

    def edges_from_dependents(self, name=None, depflag: dt.DepFlag = dt.ALL):
        """Return a list of edges connecting this node in the DAG
        to parents.

        Args:
            name (str): filter dependents by package name
            depflag: allowed dependency types
        """
        return [d for d in self._dependents.select(parent=name, depflag=depflag)]

    def edges_to_dependencies(self, name=None, depflag: dt.DepFlag = dt.ALL):
        """Return a list of edges connecting this node in the DAG
        to children.

        Args:
            name (str): filter dependencies by package name
            depflag: allowed dependency types
        """
        return [d for d in self._dependencies.select(child=name, depflag=depflag)]

    @property
    def edge_attributes(self) -> str:
        """Helper method to print edge attributes in spec literals"""
        edges = self.edges_from_dependents()
        if not edges:
            return ""

        union = DependencySpec(parent=Spec(), spec=self, depflag=0, virtuals=())
        for edge in edges:
            union.update_deptypes(edge.depflag)
            union.update_virtuals(edge.virtuals)
        deptypes_str = (
            f"deptypes={','.join(dt.flag_to_tuple(union.depflag))}" if union.depflag else ""
        )
        virtuals_str = f"virtuals={','.join(union.virtuals)}" if union.virtuals else ""
        if not deptypes_str and not virtuals_str:
            return ""
        result = f"{deptypes_str} {virtuals_str}".strip()
        return f"[{result}]"

    def dependencies(
        self, name=None, deptype: Union[dt.DepTypes, dt.DepFlag] = dt.ALL
    ) -> List["Spec"]:
        """Return a list of direct dependencies (nodes in the DAG).

        Args:
            name (str): filter dependencies by package name
            deptype: allowed dependency types
        """
        if not isinstance(deptype, dt.DepFlag):
            deptype = dt.canonicalize(deptype)
        return [d.spec for d in self.edges_to_dependencies(name, depflag=deptype)]

    def dependents(
        self, name=None, deptype: Union[dt.DepTypes, dt.DepFlag] = dt.ALL
    ) -> List["Spec"]:
        """Return a list of direct dependents (nodes in the DAG).

        Args:
            name (str): filter dependents by package name
            deptype: allowed dependency types
        """
        if not isinstance(deptype, dt.DepFlag):
            deptype = dt.canonicalize(deptype)
        return [d.parent for d in self.edges_from_dependents(name, depflag=deptype)]

    def _dependencies_dict(self, depflag: dt.DepFlag = dt.ALL):
        """Return a dictionary, keyed by package name, of the direct
        dependencies.

        Each value in the dictionary is a list of edges.

        Args:
            deptype: allowed dependency types
        """
        _sort_fn = lambda x: (x.spec.name, _sort_by_dep_types(x))
        _group_fn = lambda x: x.spec.name
        selected_edges = self._dependencies.select(depflag=depflag)
        result = {}
        for key, group in itertools.groupby(sorted(selected_edges, key=_sort_fn), key=_group_fn):
            result[key] = list(group)
        return result

    def _add_flag(self, name, value, propagate):
        """Called by the parser to add a known flag.
        Known flags currently include "arch"
        """

        # If the == syntax is used to propagate the spec architecture
        # This is an error
        architecture_names = [
            "arch",
            "architecture",
            "platform",
            "os",
            "operating_system",
            "target",
        ]
        if propagate and name in architecture_names:
            raise ArchitecturePropagationError(
                "Unable to propagate the architecture failed." " Use a '=' instead."
            )

        valid_flags = FlagMap.valid_compiler_flags()
        if name == "arch" or name == "architecture":
            parts = tuple(value.split("-"))
            plat, os, tgt = parts if len(parts) == 3 else (None, None, value)
            self._set_architecture(platform=plat, os=os, target=tgt)
        elif name == "platform":
            self._set_architecture(platform=value)
        elif name == "os" or name == "operating_system":
            self._set_architecture(os=value)
        elif name == "target":
            self._set_architecture(target=value)
        elif name in valid_flags:
            assert self.compiler_flags is not None
            flags_and_propagation = spack.compiler.tokenize_flags(value, propagate)
            for flag, propagation in flags_and_propagation:
                self.compiler_flags.add_flag(name, flag, propagation)
        else:
            # FIXME:
            # All other flags represent variants. 'foo=true' and 'foo=false'
            # map to '+foo' and '~foo' respectively. As such they need a
            # BoolValuedVariant instance.
            if str(value).upper() == "TRUE" or str(value).upper() == "FALSE":
                self.variants[name] = vt.BoolValuedVariant(name, value, propagate)
            else:
                self.variants[name] = vt.AbstractVariant(name, value, propagate)

    def _set_architecture(self, **kwargs):
        """Called by the parser to set the architecture."""
        arch_attrs = ["platform", "os", "target"]
        if self.architecture and self.architecture.concrete:
            raise DuplicateArchitectureError(
                "Spec for '%s' cannot have two architectures." % self.name
            )

        if not self.architecture:
            new_vals = tuple(kwargs.get(arg, None) for arg in arch_attrs)
            self.architecture = ArchSpec(new_vals)
        else:
            new_attrvals = [(a, v) for a, v in kwargs.items() if a in arch_attrs]
            for new_attr, new_value in new_attrvals:
                if getattr(self.architecture, new_attr):
                    raise DuplicateArchitectureError(
                        "Spec for '%s' cannot have two '%s' specified "
                        "for its architecture" % (self.name, new_attr)
                    )
                else:
                    setattr(self.architecture, new_attr, new_value)

    def _add_dependency(self, spec: "Spec", *, depflag: dt.DepFlag, virtuals: Tuple[str, ...]):
        """Called by the parser to add another spec as a dependency."""
        if spec.name not in self._dependencies or not spec.name:
            self.add_dependency_edge(spec, depflag=depflag, virtuals=virtuals)
            return

        # Keep the intersection of constraints when a dependency is added multiple times.
        # The only restriction, currently, is keeping the same dependency type
        orig = self._dependencies[spec.name]
        try:
            dspec = next(dspec for dspec in orig if depflag == dspec.depflag)
        except StopIteration:
            edge_attrs = f"deptypes={dt.flag_to_chars(depflag).strip()}"
            required_dep_str = f"^[{edge_attrs}] {str(spec)}"

            raise DuplicateDependencyError(
                f"{spec.name} is a duplicate dependency, with conflicting dependency types\n"
                f"\t'{str(self)}' cannot depend on '{required_dep_str}'"
            )

        try:
            dspec.spec.constrain(spec)
            dspec.update_virtuals(virtuals=virtuals)
        except spack.error.UnsatisfiableSpecError:
            raise DuplicateDependencyError(
                f"Cannot depend on incompatible specs '{dspec.spec}' and '{spec}'"
            )

    def add_dependency_edge(
        self, dependency_spec: "Spec", *, depflag: dt.DepFlag, virtuals: Tuple[str, ...]
    ):
        """Add a dependency edge to this spec.

        Args:
            dependency_spec: spec of the dependency
            deptypes: dependency types for this edge
            virtuals: virtuals provided by this edge
        """
        # Check if we need to update edges that are already present
        selected = self._dependencies.select(child=dependency_spec.name)
        for edge in selected:
            has_errors, details = False, []
            msg = f"cannot update the edge from {edge.parent.name} to {edge.spec.name}"
            if edge.depflag & depflag:
                has_errors = True
                details.append(
                    (
                        f"{edge.parent.name} has already an edge matching any"
                        f" of these types {depflag}"
                    )
                )

            if any(v in edge.virtuals for v in virtuals):
                has_errors = True
                details.append(
                    (
                        f"{edge.parent.name} has already an edge matching any"
                        f" of these virtuals {virtuals}"
                    )
                )

            if has_errors:
                raise spack.error.SpecError(msg, "\n".join(details))

        for edge in selected:
            if id(dependency_spec) == id(edge.spec):
                # If we are here, it means the edge object was previously added to
                # both the parent and the child. When we update this object they'll
                # both see the deptype modification.
                edge.update_deptypes(depflag=depflag)
                edge.update_virtuals(virtuals=virtuals)
                return

        edge = DependencySpec(self, dependency_spec, depflag=depflag, virtuals=virtuals)
        self._dependencies.add(edge)
        dependency_spec._dependents.add(edge)

    #
    # Public interface
    #
    @property
    def fullname(self):
        return (
            ("%s.%s" % (self.namespace, self.name))
            if self.namespace
            else (self.name if self.name else "")
        )

    @property
    def anonymous(self):
        return not self.name and not self.abstract_hash

    @property
    def root(self):
        """Follow dependent links and find the root of this spec's DAG.

        Spack specs have a single root (the package being installed).
        """
        # FIXME: In the case of multiple parents this property does not
        # FIXME: make sense. Should we revisit the semantics?
        if not self._dependents:
            return self
        edges_by_package = next(iter(self._dependents.values()))
        return edges_by_package[0].parent.root

    @property
    def package(self):
        assert self.concrete, "{0}: Spec.package can only be called on concrete specs".format(
            self.name
        )
        if not self._package:
            self._package = spack.repo.PATH.get(self)
        return self._package

    @property
    def package_class(self):
        """Internal package call gets only the class object for a package.
        Use this to just get package metadata.
        """
        return spack.repo.PATH.get_pkg_class(self.fullname)

    @property
    def virtual(self):
        return spack.repo.PATH.is_virtual(self.name)

    @property
    def concrete(self):
        """A spec is concrete if it describes a single build of a package.

        More formally, a spec is concrete if concretize() has been called
        on it and it has been marked `_concrete`.

        Concrete specs either can be or have been built. All constraints
        have been resolved, optional dependencies have been added or
        removed, a compiler has been chosen, and all variants have
        values.
        """
        return self._concrete

    @property
    def spliced(self):
        """Returns whether or not this Spec is being deployed as built i.e.
        whether or not this Spec has ever been spliced.
        """
        return any(s.build_spec is not s for s in self.traverse(root=True))

    @property
    def installed(self):
        """Installation status of a package.

        Returns:
            True if the package has been installed, False otherwise.
        """
        if not self.concrete:
            return False

        try:
            # If the spec is in the DB, check the installed
            # attribute of the record
            return spack.store.STORE.db.get_record(self).installed
        except KeyError:
            # If the spec is not in the DB, the method
            #  above raises a Key error
            return False

    @property
    def installed_upstream(self):
        """Whether the spec is installed in an upstream repository.

        Returns:
            True if the package is installed in an upstream, False otherwise.
        """
        if not self.concrete:
            return False

        upstream, _ = spack.store.STORE.db.query_by_spec_hash(self.dag_hash())
        return upstream

    def traverse(self, **kwargs):
        """Shorthand for :meth:`~spack.traverse.traverse_nodes`"""
        return traverse.traverse_nodes([self], **kwargs)

    def traverse_edges(self, **kwargs):
        """Shorthand for :meth:`~spack.traverse.traverse_edges`"""
        return traverse.traverse_edges([self], **kwargs)

    @property
    def short_spec(self):
        """Returns a version of the spec with the dependencies hashed
        instead of completely enumerated."""
        spec_format = "{name}{@version}{%compiler.name}{@compiler.version}"
        spec_format += "{variants}{arch=architecture}{/hash:7}"
        return self.format(spec_format)

    @property
    def cshort_spec(self):
        """Returns an auto-colorized version of ``self.short_spec``."""
        spec_format = "{name}{@version}{%compiler.name}{@compiler.version}"
        spec_format += "{variants}{arch=architecture}{/hash:7}"
        return self.cformat(spec_format)

    @property
    def prefix(self):
        if not self._concrete:
            raise spack.error.SpecError("Spec is not concrete: " + str(self))

        if self._prefix is None:
            upstream, record = spack.store.STORE.db.query_by_spec_hash(self.dag_hash())
            if record and record.path:
                self.prefix = record.path
            else:
                self.prefix = spack.store.STORE.layout.path_for_spec(self)
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = spack.util.prefix.Prefix(llnl.path.convert_to_platform_path(value))

    def spec_hash(self, hash):
        """Utility method for computing different types of Spec hashes.

        Arguments:
            hash (spack.hash_types.SpecHashDescriptor): type of hash to generate.
        """
        # TODO: currently we strip build dependencies by default.  Rethink
        # this when we move to using package hashing on all specs.
        if hash.override is not None:
            return hash.override(self)
        node_dict = self.to_node_dict(hash=hash)
        json_text = sjson.dump(node_dict)
        # This implements "frankenhashes", preserving the last 7 characters of the
        # original hash when splicing so that we can avoid relocation issues
        out = spack.util.hash.b32_hash(json_text)
        if self.build_spec is not self:
            return out[:-7] + self.build_spec.spec_hash(hash)[-7:]
        return out

    def _cached_hash(self, hash, length=None, force=False):
        """Helper function for storing a cached hash on the spec.

        This will run spec_hash() with the deptype and package_hash
        parameters, and if this spec is concrete, it will store the value
        in the supplied attribute on this spec.

        Arguments:
            hash (spack.hash_types.SpecHashDescriptor): type of hash to generate.
            length (int): length of hash prefix to return (default is full hash string)
            force (bool): cache the hash even if spec is not concrete (default False)
        """
        if not hash.attr:
            return self.spec_hash(hash)[:length]

        hash_string = getattr(self, hash.attr, None)
        if hash_string:
            return hash_string[:length]
        else:
            hash_string = self.spec_hash(hash)
            if force or self.concrete:
                setattr(self, hash.attr, hash_string)

            return hash_string[:length]

    def package_hash(self):
        """Compute the hash of the contents of the package for this node"""
        # Concrete specs with the old DAG hash did not have the package hash, so we do
        # not know what the package looked like at concretization time
        if self.concrete and not self._package_hash:
            raise ValueError(
                "Cannot call package_hash() on concrete specs with the old dag_hash()"
            )

        return self._cached_hash(ht.package_hash)

    def dag_hash(self, length=None):
        """This is Spack's default hash, used to identify installations.

        Same as the full hash (includes package hash and build/link/run deps).
        Tells us when package files and any dependencies have changes.

        NOTE: Versions of Spack prior to 0.18 only included link and run deps.

        """
        return self._cached_hash(ht.dag_hash, length)

    def process_hash(self, length=None):
        """Hash used to transfer specs among processes.

        This hash includes build and test dependencies and is only used to
        serialize a spec and pass it around among processes.
        """
        return self._cached_hash(ht.process_hash, length)

    def dag_hash_bit_prefix(self, bits):
        """Get the first <bits> bits of the DAG hash as an integer type."""
        return spack.util.hash.base32_prefix_bits(self.dag_hash(), bits)

    def process_hash_bit_prefix(self, bits):
        """Get the first <bits> bits of the DAG hash as an integer type."""
        return spack.util.hash.base32_prefix_bits(self.process_hash(), bits)

    def _lookup_hash(self):
        """Lookup just one spec with an abstract hash, returning a spec from the the environment,
        store, or finally, binary caches."""
        import spack.environment

        active_env = spack.environment.active_environment()

        # First env, then store, then binary cache
        matches = (
            (active_env.all_matching_specs(self) if active_env else [])
            or spack.store.STORE.db.query(self, installed=any)
            or spack.binary_distribution.BinaryCacheQuery(True)(self)
        )

        if not matches:
            raise InvalidHashError(self, self.abstract_hash)

        if len(matches) != 1:
            raise spack.spec.AmbiguousHashError(
                f"Multiple packages specify hash beginning '{self.abstract_hash}'.", *matches
            )

        return matches[0]

    def lookup_hash(self):
        """Given a spec with an abstract hash, return a copy of the spec with all properties and
        dependencies by looking up the hash in the environment, store, or finally, binary caches.
        This is non-destructive."""
        if self.concrete or not any(node.abstract_hash for node in self.traverse()):
            return self

        spec = self.copy(deps=False)
        # root spec is replaced
        if spec.abstract_hash:
            spec._dup(self._lookup_hash())
            return spec

        # Get dependencies that need to be replaced
        for node in self.traverse(root=False):
            if node.abstract_hash:
                spec._add_dependency(node._lookup_hash(), depflag=0, virtuals=())

        # reattach nodes that were not otherwise satisfied by new dependencies
        for node in self.traverse(root=False):
            if not any(n.satisfies(node) for n in spec.traverse()):
                spec._add_dependency(node.copy(), depflag=0, virtuals=())

        return spec

    def replace_hash(self):
        """Given a spec with an abstract hash, attempt to populate all properties and dependencies
        by looking up the hash in the environment, store, or finally, binary caches.
        This is destructive."""

        if not any(node for node in self.traverse(order="post") if node.abstract_hash):
            return

        self._dup(self.lookup_hash())

    def to_node_dict(self, hash=ht.dag_hash):
        """Create a dictionary representing the state of this Spec.

        ``to_node_dict`` creates the content that is eventually hashed by
        Spack to create identifiers like the DAG hash (see
        ``dag_hash()``).  Example result of ``to_node_dict`` for the
        ``sqlite`` package::

            {
                'sqlite': {
                    'version': '3.28.0',
                    'arch': {
                        'platform': 'darwin',
                        'platform_os': 'mojave',
                        'target': 'x86_64',
                    },
                    'compiler': {
                        'name': 'apple-clang',
                        'version': '10.0.0',
                    },
                    'namespace': 'builtin',
                    'parameters': {
                        'fts': 'true',
                        'functions': 'false',
                        'cflags': [],
                        'cppflags': [],
                        'cxxflags': [],
                        'fflags': [],
                        'ldflags': [],
                        'ldlibs': [],
                    },
                    'dependencies': {
                        'readline': {
                            'hash': 'zvaa4lhlhilypw5quj3akyd3apbq5gap',
                            'type': ['build', 'link'],
                        }
                    },
                }
            }

        Note that the dictionary returned does *not* include the hash of
        the *root* of the spec, though it does include hashes for each
        dependency, and (optionally) the package file corresponding to
        each node.

        See ``to_dict()`` for a "complete" spec hash, with hashes for
        each node and nodes for each dependency (instead of just their
        hashes).

        Arguments:
            hash (spack.hash_types.SpecHashDescriptor) type of hash to generate.
        """
        d = syaml.syaml_dict()

        d["name"] = self.name

        if self.versions:
            d.update(self.versions.to_dict())

        if self.architecture:
            d.update(self.architecture.to_dict())

        if self.compiler:
            d.update(self.compiler.to_dict())

        if self.namespace:
            d["namespace"] = self.namespace

        params = syaml.syaml_dict(sorted(v.yaml_entry() for _, v in self.variants.items()))

        # Only need the string compiler flag for yaml file
        params.update(
            sorted(
                self.compiler_flags.yaml_entry(flag_type)
                for flag_type in self.compiler_flags.keys()
            )
        )

        if params:
            d["parameters"] = params

        if params and not self.concrete:
            flag_names = [
                name
                for name, flags in self.compiler_flags.items()
                if any(x.propagate for x in flags)
            ]
            d["propagate"] = sorted(
                itertools.chain(
                    [v.name for v in self.variants.values() if v.propagate], flag_names
                )
            )

        if self.external:
            d["external"] = syaml.syaml_dict(
                [
                    ("path", self.external_path),
                    ("module", self.external_modules),
                    ("extra_attributes", self.extra_attributes),
                ]
            )

        if not self._concrete:
            d["concrete"] = False

        if "patches" in self.variants:
            variant = self.variants["patches"]
            if hasattr(variant, "_patches_in_order_of_appearance"):
                d["patches"] = variant._patches_in_order_of_appearance

        if (
            self._concrete
            and hash.package_hash
            and hasattr(self, "_package_hash")
            and self._package_hash
        ):
            # We use the attribute here instead of `self.package_hash()` because this
            # should *always* be assignhed at concretization time. We don't want to try
            # to compute a package hash for concrete spec where a) the package might not
            # exist, or b) the `dag_hash` didn't include the package hash when the spec
            # was concretized.
            package_hash = self._package_hash

            # Full hashes are in bytes
            if not isinstance(package_hash, str) and isinstance(package_hash, bytes):
                package_hash = package_hash.decode("utf-8")
            d["package_hash"] = package_hash

        # Note: Relies on sorting dict by keys later in algorithm.
        deps = self._dependencies_dict(depflag=hash.depflag)
        if deps:
            deps_list = []
            for name, edges_for_name in sorted(deps.items()):
                name_tuple = ("name", name)
                for dspec in edges_for_name:
                    hash_tuple = (hash.name, dspec.spec._cached_hash(hash))
                    parameters_tuple = (
                        "parameters",
                        syaml.syaml_dict(
                            (
                                ("deptypes", dt.flag_to_tuple(dspec.depflag)),
                                ("virtuals", dspec.virtuals),
                            )
                        ),
                    )
                    ordered_entries = [name_tuple, hash_tuple, parameters_tuple]
                    deps_list.append(syaml.syaml_dict(ordered_entries))
            d["dependencies"] = deps_list

        # Name is included in case this is replacing a virtual.
        if self._build_spec:
            d["build_spec"] = syaml.syaml_dict(
                [("name", self.build_spec.name), (hash.name, self.build_spec._cached_hash(hash))]
            )
        return d

    def to_dict(self, hash=ht.dag_hash):
        """Create a dictionary suitable for writing this spec to YAML or JSON.

        This dictionaries like the one that is ultimately written to a
        ``spec.json`` file in each Spack installation directory.  For
        example, for sqlite::

            {
            "spec": {
                "_meta": {
                "version": 2
                },
                "nodes": [
                {
                    "name": "sqlite",
                    "version": "3.34.0",
                    "arch": {
                    "platform": "darwin",
                    "platform_os": "catalina",
                    "target": "x86_64"
                    },
                    "compiler": {
                    "name": "apple-clang",
                    "version": "11.0.0"
                    },
                    "namespace": "builtin",
                    "parameters": {
                    "column_metadata": true,
                    "fts": true,
                    "functions": false,
                    "rtree": false,
                    "cflags": [],
                    "cppflags": [],
                    "cxxflags": [],
                    "fflags": [],
                    "ldflags": [],
                    "ldlibs": []
                    },
                    "dependencies": [
                    {
                        "name": "readline",
                        "hash": "4f47cggum7p4qmp3xna4hi547o66unva",
                        "type": [
                        "build",
                        "link"
                        ]
                    },
                    {
                        "name": "zlib",
                        "hash": "uvgh6p7rhll4kexqnr47bvqxb3t33jtq",
                        "type": [
                        "build",
                        "link"
                        ]
                    }
                    ],
                    "hash": "tve45xfqkfgmzwcyfetze2z6syrg7eaf",
                },
                    # ... more node dicts for readline and its dependencies ...
                ]
            }

        Note that this dictionary starts with the 'spec' key, and what
        follows is a list starting with the root spec, followed by its
        dependencies in preorder.  Each node in the list also has a
        'hash' key that contains the hash of the node *without* the hash
        field included.

        In the example, the package content hash is not included in the
        spec, but if ``package_hash`` were true there would be an
        additional field on each node called ``package_hash``.

        ``from_dict()`` can be used to read back in a spec that has been
        converted to a dictionary, serialized, and read back in.

        Arguments:
            deptype (tuple or str): dependency types to include when
                traversing the spec.
            package_hash (bool): whether to include package content
                hashes in the dictionary.

        """
        node_list = []  # Using a list to preserve preorder traversal for hash.
        hash_set = set()
        for s in self.traverse(order="pre", deptype=hash.depflag):
            spec_hash = s._cached_hash(hash)

            if spec_hash not in hash_set:
                node_list.append(s.node_dict_with_hashes(hash))
                hash_set.add(spec_hash)

            if s.build_spec is not s:
                build_spec_list = s.build_spec.to_dict(hash)["spec"]["nodes"]
                for node in build_spec_list:
                    node_hash = node[hash.name]
                    if node_hash not in hash_set:
                        node_list.append(node)
                        hash_set.add(node_hash)

        meta_dict = syaml.syaml_dict([("version", SPECFILE_FORMAT_VERSION)])
        inner_dict = syaml.syaml_dict([("_meta", meta_dict), ("nodes", node_list)])
        spec_dict = syaml.syaml_dict([("spec", inner_dict)])
        return spec_dict

    def node_dict_with_hashes(self, hash=ht.dag_hash):
        """Returns a node_dict of this spec with the dag hash added.  If this
        spec is concrete, the full hash is added as well.  If 'build' is in
        the hash_type, the build hash is also added."""
        node = self.to_node_dict(hash)
        # All specs have at least a DAG hash
        node[ht.dag_hash.name] = self.dag_hash()

        if not self.concrete:
            node["concrete"] = False

        # we can also give them other hash types if we want
        if hash.name != ht.dag_hash.name:
            node[hash.name] = self._cached_hash(hash)

        return node

    def to_yaml(self, stream=None, hash=ht.dag_hash):
        return syaml.dump(self.to_dict(hash), stream=stream, default_flow_style=False)

    def to_json(self, stream=None, hash=ht.dag_hash):
        return sjson.dump(self.to_dict(hash), stream)

    @staticmethod
    def from_specfile(path):
        """Construct a spec from a JSON or YAML spec file path"""
        with open(path, "r") as fd:
            file_content = fd.read()
            if path.endswith(".json"):
                return Spec.from_json(file_content)
            return Spec.from_yaml(file_content)

    @staticmethod
    def override(init_spec, change_spec):
        # TODO: this doesn't account for the case where the changed spec
        # (and the user spec) have dependencies
        new_spec = init_spec.copy()
        package_cls = spack.repo.PATH.get_pkg_class(new_spec.name)
        if change_spec.versions and not change_spec.versions == vn.any_version:
            new_spec.versions = change_spec.versions
        for variant, value in change_spec.variants.items():
            if variant in package_cls.variants:
                if variant in new_spec.variants:
                    new_spec.variants.substitute(value)
                else:
                    new_spec.variants[variant] = value
            else:
                raise ValueError("{0} is not a variant of {1}".format(variant, new_spec.name))
        if change_spec.compiler:
            new_spec.compiler = change_spec.compiler
        if change_spec.compiler_flags:
            for flagname, flagvals in change_spec.compiler_flags.items():
                new_spec.compiler_flags[flagname] = flagvals
        if change_spec.architecture:
            new_spec.architecture = ArchSpec.override(
                new_spec.architecture, change_spec.architecture
            )
        return new_spec

    @staticmethod
    def from_literal(spec_dict, normal=True):
        """Builds a Spec from a dictionary containing the spec literal.

        The dictionary must have a single top level key, representing the root,
        and as many secondary level keys as needed in the spec.

        The keys can be either a string or a Spec or a tuple containing the
        Spec and the dependency types.

        Args:
            spec_dict (dict): the dictionary containing the spec literal
            normal (bool): if True the same key appearing at different levels
                of the ``spec_dict`` will map to the same object in memory.

        Examples:
            A simple spec ``foo`` with no dependencies:

            .. code-block:: python

                {'foo': None}

            A spec ``foo`` with a ``(build, link)`` dependency ``bar``:

            .. code-block:: python

                {'foo':
                    {'bar:build,link': None}}

            A spec with a diamond dependency and various build types:

            .. code-block:: python

                {'dt-diamond': {
                    'dt-diamond-left:build,link': {
                        'dt-diamond-bottom:build': None
                    },
                    'dt-diamond-right:build,link': {
                        'dt-diamond-bottom:build,link,run': None
                    }
                }}

            The same spec with a double copy of ``dt-diamond-bottom`` and
            no diamond structure:

            .. code-block:: python

                {'dt-diamond': {
                    'dt-diamond-left:build,link': {
                        'dt-diamond-bottom:build': None
                    },
                    'dt-diamond-right:build,link': {
                        'dt-diamond-bottom:build,link,run': None
                    }
                }, normal=False}

            Constructing a spec using a Spec object as key:

            .. code-block:: python

                mpich = Spec('mpich')
                libelf = Spec('libelf@1.8.11')
                expected_normalized = Spec.from_literal({
                    'mpileaks': {
                        'callpath': {
                            'dyninst': {
                                'libdwarf': {libelf: None},
                                libelf: None
                            },
                            mpich: None
                        },
                        mpich: None
                    },
                })

        """

        # Maps a literal to a Spec, to be sure we are reusing the same object
        spec_cache = LazySpecCache()

        def spec_builder(d):
            # The invariant is that the top level dictionary must have
            # only one key
            assert len(d) == 1

            # Construct the top-level spec
            spec_like, dep_like = next(iter(d.items()))

            # If the requirements was for unique nodes (default)
            # then re-use keys from the local cache. Otherwise build
            # a new node every time.
            if not isinstance(spec_like, Spec):
                spec = spec_cache[spec_like] if normal else Spec(spec_like)
            else:
                spec = spec_like

            if dep_like is None:
                return spec

            def name_and_dependency_types(s: str) -> Tuple[str, dt.DepFlag]:
                """Given a key in the dictionary containing the literal,
                extracts the name of the spec and its dependency types.

                Args:
                    s: key in the dictionary containing the literal
                """
                t = s.split(":")

                if len(t) > 2:
                    msg = 'more than one ":" separator in key "{0}"'
                    raise KeyError(msg.format(s))

                name = t[0]
                if len(t) == 2:
                    depflag = dt.flag_from_strings(dep_str.strip() for dep_str in t[1].split(","))
                else:
                    depflag = 0
                return name, depflag

            def spec_and_dependency_types(
                s: Union[Spec, Tuple[Spec, str]]
            ) -> Tuple[Spec, dt.DepFlag]:
                """Given a non-string key in the literal, extracts the spec
                and its dependency types.

                Args:
                    s: either a Spec object, or a tuple of Spec and string of dependency types
                """
                if isinstance(s, Spec):
                    return s, 0

                spec_obj, dtypes = s
                return spec_obj, dt.flag_from_strings(dt.strip() for dt in dtypes.split(","))

            # Recurse on dependencies
            for s, s_dependencies in dep_like.items():
                if isinstance(s, str):
                    dag_node, dep_flag = name_and_dependency_types(s)
                else:
                    dag_node, dep_flag = spec_and_dependency_types(s)

                dependency_spec = spec_builder({dag_node: s_dependencies})
                spec._add_dependency(dependency_spec, depflag=dep_flag, virtuals=())

            return spec

        return spec_builder(spec_dict)

    @staticmethod
    def from_dict(data):
        """Construct a spec from JSON/YAML.

        Args:
            data: a nested dict/list data structure read from YAML or JSON.
        """
        # Legacy specfile format
        if isinstance(data["spec"], list):
            spec = SpecfileV1.load(data)
        elif int(data["spec"]["_meta"]["version"]) == 2:
            spec = SpecfileV2.load(data)
        elif int(data["spec"]["_meta"]["version"]) == 3:
            spec = SpecfileV3.load(data)
        else:
            spec = SpecfileV4.load(data)

        # Any git version should
        for s in spec.traverse():
            s.attach_git_version_lookup()

        return spec

    @staticmethod
    def from_yaml(stream):
        """Construct a spec from YAML.

        Args:
            stream: string or file object to read from.
        """
        data = syaml.load(stream)
        return Spec.from_dict(data)

    @staticmethod
    def from_json(stream):
        """Construct a spec from JSON.

        Args:
            stream: string or file object to read from.
        """
        try:
            data = sjson.load(stream)
            return Spec.from_dict(data)
        except Exception as e:
            raise sjson.SpackJSONError("error parsing JSON spec:", str(e)) from e

    @staticmethod
    def extract_json_from_clearsig(data):
        m = CLEARSIGN_FILE_REGEX.search(data)
        if m:
            return sjson.load(m.group(1))
        return sjson.load(data)

    @staticmethod
    def from_signed_json(stream):
        """Construct a spec from clearsigned json spec file.

        Args:
            stream: string or file object to read from.
        """
        data = stream
        if hasattr(stream, "read"):
            data = stream.read()

        extracted_json = Spec.extract_json_from_clearsig(data)
        return Spec.from_dict(extracted_json)

    @staticmethod
    def from_detection(spec_str, extra_attributes=None):
        """Construct a spec from a spec string determined during external
        detection and attach extra attributes to it.

        Args:
            spec_str (str): spec string
            extra_attributes (dict): dictionary containing extra attributes

        Returns:
            spack.spec.Spec: external spec
        """
        s = Spec(spec_str)
        extra_attributes = syaml.sorted_dict(extra_attributes or {})
        # This is needed to be able to validate multi-valued variants,
        # otherwise they'll still be abstract in the context of detection.
        vt.substitute_abstract_variants(s)
        s.extra_attributes = extra_attributes
        return s

    def validate_detection(self):
        """Validate the detection of an external spec.

        This method is used as part of Spack's detection protocol, and is
        not meant for client code use.
        """
        # Assert that _extra_attributes is a Mapping and not None,
        # which likely means the spec was created with Spec.from_detection
        msg = 'cannot validate "{0}" since it was not created ' "using Spec.from_detection".format(
            self
        )
        assert isinstance(self.extra_attributes, collections.abc.Mapping), msg

        # Validate the spec calling a package specific method
        pkg_cls = spack.repo.PATH.get_pkg_class(self.name)
        validate_fn = getattr(pkg_cls, "validate_detected_spec", lambda x, y: None)
        validate_fn(self, self.extra_attributes)

    def _concretize_helper(self, concretizer, presets=None, visited=None):
        """Recursive helper function for concretize().
        This concretizes everything bottom-up.  As things are
        concretized, they're added to the presets, and ancestors
        will prefer the settings of their children.
        """
        if presets is None:
            presets = {}
        if visited is None:
            visited = set()

        if self.name in visited:
            return False

        if self.concrete:
            visited.add(self.name)
            return False

        changed = False

        # Concretize deps first -- this is a bottom-up process.
        for name in sorted(self._dependencies):
            # WARNING: This function is an implementation detail of the
            # WARNING: original concretizer. Since with that greedy
            # WARNING: algorithm we don't allow multiple nodes from
            # WARNING: the same package in a DAG, here we hard-code
            # WARNING: using index 0 i.e. we assume that we have only
            # WARNING: one edge from package "name"
            changed |= self._dependencies[name][0].spec._concretize_helper(
                concretizer, presets, visited
            )

        if self.name in presets:
            changed |= self.constrain(presets[self.name])
        else:
            # Concretize virtual dependencies last.  Because they're added
            # to presets below, their constraints will all be merged, but we'll
            # still need to select a concrete package later.
            if not self.virtual:
                changed |= any(
                    (
                        concretizer.concretize_develop(self),  # special variant
                        concretizer.concretize_architecture(self),
                        concretizer.concretize_compiler(self),
                        concretizer.adjust_target(self),
                        # flags must be concretized after compiler
                        concretizer.concretize_compiler_flags(self),
                        concretizer.concretize_version(self),
                        concretizer.concretize_variants(self),
                    )
                )
            presets[self.name] = self

        visited.add(self.name)
        return changed

    def _replace_with(self, concrete):
        """Replace this virtual spec with a concrete spec."""
        assert self.virtual
        virtuals = (self.name,)
        for dep_spec in itertools.chain.from_iterable(self._dependents.values()):
            dependent = dep_spec.parent
            depflag = dep_spec.depflag

            # remove self from all dependents, unless it is already removed
            if self.name in dependent._dependencies:
                del dependent._dependencies.edges[self.name]

            # add the replacement, unless it is already a dep of dependent.
            if concrete.name not in dependent._dependencies:
                dependent._add_dependency(concrete, depflag=depflag, virtuals=virtuals)
            else:
                dependent.edges_to_dependencies(name=concrete.name)[0].update_virtuals(
                    virtuals=virtuals
                )

    def _expand_virtual_packages(self, concretizer):
        """Find virtual packages in this spec, replace them with providers,
        and normalize again to include the provider's (potentially virtual)
        dependencies.  Repeat until there are no virtual deps.

        Precondition: spec is normalized.

        .. todo::

           If a provider depends on something that conflicts with
           other dependencies in the spec being expanded, this can
           produce a conflicting spec.  For example, if mpich depends
           on hwloc@:1.3 but something in the spec needs hwloc1.4:,
           then we should choose an MPI other than mpich.  Cases like
           this are infrequent, but should implement this before it is
           a problem.
        """
        # Make an index of stuff this spec already provides
        self_index = spack.provider_index.ProviderIndex(
            repository=spack.repo.PATH, specs=self.traverse(), restrict=True
        )
        changed = False
        done = False

        while not done:
            done = True
            for spec in list(self.traverse()):
                replacement = None
                if spec.external:
                    continue
                if spec.virtual:
                    replacement = self._find_provider(spec, self_index)
                    if replacement:
                        # TODO: may break if in-place on self but
                        # shouldn't happen if root is traversed first.
                        spec._replace_with(replacement)
                        done = False
                        break

                if not replacement:
                    # Get a list of possible replacements in order of
                    # preference.
                    candidates = concretizer.choose_virtual_or_external(spec)

                    # Try the replacements in order, skipping any that cause
                    # satisfiability problems.
                    for replacement in candidates:
                        if replacement is spec:
                            break

                        # Replace spec with the candidate and normalize
                        copy = self.copy()
                        copy[spec.name]._dup(replacement, deps=False)

                        try:
                            # If there are duplicate providers or duplicate
                            # provider deps, consolidate them and merge
                            # constraints.
                            copy.normalize(force=True)
                            break
                        except spack.error.SpecError:
                            # On error, we'll try the next replacement.
                            continue

                # If replacement is external then trim the dependencies
                if replacement.external:
                    if spec._dependencies:
                        for dep in spec.dependencies():
                            del dep._dependents.edges[spec.name]
                        changed = True
                        spec.clear_dependencies()
                    replacement.clear_dependencies()
                    replacement.architecture = self.architecture

                # TODO: could this and the stuff in _dup be cleaned up?
                def feq(cfield, sfield):
                    return (not cfield) or (cfield == sfield)

                if replacement is spec or (
                    feq(replacement.name, spec.name)
                    and feq(replacement.versions, spec.versions)
                    and feq(replacement.compiler, spec.compiler)
                    and feq(replacement.architecture, spec.architecture)
                    and feq(replacement._dependencies, spec._dependencies)
                    and feq(replacement.variants, spec.variants)
                    and feq(replacement.external_path, spec.external_path)
                    and feq(replacement.external_modules, spec.external_modules)
                ):
                    continue
                # Refine this spec to the candidate. This uses
                # replace_with AND dup so that it can work in
                # place. TODO: make this more efficient.
                if spec.virtual:
                    spec._replace_with(replacement)
                    changed = True
                if spec._dup(replacement, deps=False, cleardeps=False):
                    changed = True

                self_index.update(spec)
                done = False
                break

        return changed

    def _old_concretize(self, tests=False, deprecation_warning=True):
        """A spec is concrete if it describes one build of a package uniquely.
        This will ensure that this spec is concrete.

        Args:
            tests (list or bool): list of packages that will need test
                dependencies, or True/False for test all/none
            deprecation_warning (bool): enable or disable the deprecation
                warning for the old concretizer

        If this spec could describe more than one version, variant, or build
        of a package, this will add constraints to make it concrete.

        Some rigorous validation and checks are also performed on the spec.
        Concretizing ensures that it is self-consistent and that it's
        consistent with requirements of its packages. See flatten() and
        normalize() for more details on this.
        """
        import spack.concretize

        # Add a warning message to inform users that the original concretizer
        # will be removed
        if deprecation_warning:
            msg = (
                "the original concretizer is currently being used.\n\tUpgrade to "
                '"clingo" at your earliest convenience. The original concretizer '
                "will be removed from Spack in a future version."
            )
            warnings.warn(msg)

        self.replace_hash()

        if not self.name:
            raise spack.error.SpecError("Attempting to concretize anonymous spec")

        if self._concrete:
            return

        # take the spec apart once before starting the main concretization loop and resolving
        # deps, but don't break dependencies during concretization as the spec is built.
        user_spec_deps = self.flat_dependencies(disconnect=True)

        changed = True
        force = False
        concretizer = spack.concretize.Concretizer(self.copy())
        while changed:
            changes = (
                self.normalize(force, tests, user_spec_deps, disconnect=False),
                self._expand_virtual_packages(concretizer),
                self._concretize_helper(concretizer),
            )
            changed = any(changes)
            force = True

        visited_user_specs = set()
        for dep in self.traverse():
            visited_user_specs.add(dep.name)
            pkg_cls = spack.repo.PATH.get_pkg_class(dep.name)
            visited_user_specs.update(pkg_cls(dep).provided_virtual_names())

        extra = set(user_spec_deps.keys()).difference(visited_user_specs)
        if extra:
            raise InvalidDependencyError(self.name, extra)

        Spec.inject_patches_variant(self)

        for s in self.traverse():
            # TODO: Refactor this into a common method to build external specs
            # TODO: or turn external_path into a lazy property
            Spec.ensure_external_path_if_external(s)

        # assign hashes and mark concrete
        self._finalize_concretization()

        # If any spec in the DAG is deprecated, throw an error
        Spec.ensure_no_deprecated(self)

        # Update externals as needed
        for dep in self.traverse():
            if dep.external:
                dep.package.update_external_dependencies()

        # Now that the spec is concrete we should check if
        # there are declared conflicts
        #
        # TODO: this needs rethinking, as currently we can only express
        # TODO: internal configuration conflicts within one package.
        matches = []
        for x in self.traverse():
            if x.external:
                # external specs are already built, don't worry about whether
                # it's possible to build that configuration with Spack
                continue

            for when_spec, conflict_list in x.package_class.conflicts.items():
                if x.satisfies(when_spec):
                    for conflict_spec, msg in conflict_list:
                        if x.satisfies(conflict_spec):
                            when = when_spec.copy()
                            when.name = x.name
                            matches.append((x, conflict_spec, when, msg))
        if matches:
            raise ConflictsInSpecError(self, matches)

        # Check if we can produce an optimized binary (will throw if
        # there are declared inconsistencies)
        # No need on platform=cray because of the targeting modules
        if not self.satisfies("platform=cray"):
            self.architecture.target.optimization_flags(self.compiler)

    def _patches_assigned(self):
        """Whether patches have been assigned to this spec by the concretizer."""
        # FIXME: _patches_in_order_of_appearance is attached after concretization
        # FIXME: to store the order of patches.
        # FIXME: Probably needs to be refactored in a cleaner way.
        if "patches" not in self.variants:
            return False

        # ensure that patch state is consistent
        patch_variant = self.variants["patches"]
        assert hasattr(
            patch_variant, "_patches_in_order_of_appearance"
        ), "patches should always be assigned with a patch variant."

        return True

    @staticmethod
    def inject_patches_variant(root):
        # This dictionary will store object IDs rather than Specs as keys
        # since the Spec __hash__ will change as patches are added to them
        spec_to_patches = {}
        for s in root.traverse():
            # After concretizing, assign namespaces to anything left.
            # Note that this doesn't count as a "change".  The repository
            # configuration is constant throughout a spack run, and
            # normalize and concretize evaluate Packages using Repo.get(),
            # which respects precedence.  So, a namespace assignment isn't
            # changing how a package name would have been interpreted and
            # we can do it as late as possible to allow as much
            # compatibility across repositories as possible.
            if s.namespace is None:
                s.namespace = spack.repo.PATH.repo_for_pkg(s.name).namespace

            if s.concrete:
                continue

            # Add any patches from the package to the spec.
            patches = set()
            for cond, patch_list in s.package_class.patches.items():
                if s.satisfies(cond):
                    for patch in patch_list:
                        patches.add(patch)
            if patches:
                spec_to_patches[id(s)] = patches

        # Also record all patches required on dependencies by
        # depends_on(..., patch=...)
        for dspec in root.traverse_edges(deptype=all, cover="edges", root=False):
            if dspec.spec.concrete:
                continue

            pkg_deps = dspec.parent.package_class.dependencies

            patches = []
            for cond, deps_by_name in pkg_deps.items():
                if not dspec.parent.satisfies(cond):
                    continue

                dependency = deps_by_name.get(dspec.spec.name)
                if not dependency:
                    continue

                for pcond, patch_list in dependency.patches.items():
                    if dspec.spec.satisfies(pcond):
                        patches.extend(patch_list)

            if patches:
                all_patches = spec_to_patches.setdefault(id(dspec.spec), set())
                for patch in patches:
                    all_patches.add(patch)

        for spec in root.traverse():
            if id(spec) not in spec_to_patches:
                continue

            patches = list(lang.dedupe(spec_to_patches[id(spec)]))
            mvar = spec.variants.setdefault("patches", vt.MultiValuedVariant("patches", ()))
            mvar.value = tuple(p.sha256 for p in patches)
            # FIXME: Monkey patches mvar to store patches order
            full_order_keys = list(tuple(p.ordering_key) + (p.sha256,) for p in patches)
            ordered_hashes = sorted(full_order_keys)
            tty.debug(
                "Ordered hashes [{0}]: ".format(spec.name)
                + ", ".join("/".join(str(e) for e in t) for t in ordered_hashes)
            )
            mvar._patches_in_order_of_appearance = list(t[-1] for t in ordered_hashes)

    @staticmethod
    def ensure_external_path_if_external(external_spec):
        if external_spec.external_modules and not external_spec.external_path:
            compiler = spack.compilers.compiler_for_spec(
                external_spec.compiler, external_spec.architecture
            )
            for mod in compiler.modules:
                md.load_module(mod)

            # Get the path from the module the package can override the default
            # (this is mostly needed for Cray)
            pkg_cls = spack.repo.PATH.get_pkg_class(external_spec.name)
            package = pkg_cls(external_spec)
            external_spec.external_path = getattr(
                package, "external_prefix", md.path_from_modules(external_spec.external_modules)
            )

    @staticmethod
    def ensure_no_deprecated(root):
        """Raise if a deprecated spec is in the dag.

        Args:
            root (Spec): root spec to be analyzed

        Raises:
            SpecDeprecatedError: if any deprecated spec is found
        """
        deprecated = []
        with spack.store.STORE.db.read_transaction():
            for x in root.traverse():
                _, rec = spack.store.STORE.db.query_by_spec_hash(x.dag_hash())
                if rec and rec.deprecated_for:
                    deprecated.append(rec)
        if deprecated:
            msg = "\n    The following specs have been deprecated"
            msg += " in favor of specs with the hashes shown:\n"
            for rec in deprecated:
                msg += "        %s  --> %s\n" % (rec.spec, rec.deprecated_for)
            msg += "\n"
            msg += "    For each package listed, choose another spec\n"
            raise SpecDeprecatedError(msg)

    def _new_concretize(self, tests=False):
        import spack.solver.asp

        self.replace_hash()

        for node in self.traverse():
            if not node.name:
                raise spack.error.SpecError(
                    f"Spec {node} has no name; cannot concretize an anonymous spec"
                )

        if self._concrete:
            return

        allow_deprecated = spack.config.get("config:deprecated", False)
        solver = spack.solver.asp.Solver()
        result = solver.solve([self], tests=tests, allow_deprecated=allow_deprecated)

        # take the best answer
        opt, i, answer = min(result.answers)
        name = self.name
        # TODO: Consolidate this code with similar code in solve.py
        if self.virtual:
            providers = [spec.name for spec in answer.values() if spec.package.provides(name)]
            name = providers[0]

        node = spack.solver.asp.SpecBuilder.make_node(pkg=name)
        assert (
            node in answer
        ), f"cannot find {name} in the list of specs {','.join([n.pkg for n in answer.keys()])}"

        concretized = answer[node]
        self._dup(concretized)

    def concretize(self, tests=False):
        """Concretize the current spec.

        Args:
            tests (bool or list): if False disregard 'test' dependencies,
                if a list of names activate them for the packages in the list,
                if True activate 'test' dependencies for all packages.
        """
        if spack.config.get("config:concretizer", "clingo") == "clingo":
            self._new_concretize(tests)
        else:
            self._old_concretize(tests)

    def _mark_root_concrete(self, value=True):
        """Mark just this spec (not dependencies) concrete."""
        if (not value) and self.concrete and self.installed:
            return
        self._normal = value
        self._concrete = value
        self._validate_version()

    def _validate_version(self):
        # Specs that were concretized with just a git sha as version, without associated
        # Spack version, get their Spack version mapped to develop. This should only apply
        # when reading specs concretized with Spack 0.19 or earlier. Currently Spack always
        # ensures that GitVersion specs have an associated Spack version.
        v = self.versions.concrete
        if not isinstance(v, vn.GitVersion):
            return

        try:
            v.ref_version
        except vn.VersionLookupError:
            before = self.cformat("{name}{@version}{/hash:7}")
            v._ref_version = vn.StandardVersion.from_string("develop")
            tty.debug(
                f"the git sha of {before} could not be resolved to spack version; "
                f"it has been replaced by {self.cformat('{name}{@version}{/hash:7}')}."
            )

    def _mark_concrete(self, value=True):
        """Mark this spec and its dependencies as concrete.

        Only for internal use -- client code should use "concretize"
        unless there is a need to force a spec to be concrete.
        """
        # if set to false, clear out all hashes (set to None or remove attr)
        # may need to change references to respect None
        for s in self.traverse():
            if (not value) and s.concrete and s.installed:
                continue
            elif not value:
                s.clear_cached_hashes()
            s._mark_root_concrete(value)

    def _finalize_concretization(self):
        """Assign hashes to this spec, and mark it concrete.

        There are special semantics to consider for `package_hash`, because we can't
        call it on *already* concrete specs, but we need to assign it *at concretization
        time* to just-concretized specs. So, the concretizer must assign the package
        hash *before* marking their specs concrete (so that we know which specs were
        already concrete before this latest concretization).

        `dag_hash` is also tricky, since it cannot compute `package_hash()` lazily.
        Because `package_hash` needs to be assigned *at concretization time*,
        `to_node_dict()` can't just assume that it can compute `package_hash` itself
        -- it needs to either see or not see a `_package_hash` attribute.

        Rules of thumb for `package_hash`:
          1. Old-style concrete specs from *before* `dag_hash` included `package_hash`
             will not have a `_package_hash` attribute at all.
          2. New-style concrete specs will have a `_package_hash` assigned at
             concretization time.
          3. Abstract specs will not have a `_package_hash` attribute at all.

        """
        for spec in self.traverse():
            # Already concrete specs either already have a package hash (new dag_hash())
            # or they never will b/c we can't know it (old dag_hash()). Skip them.
            #
            # We only assign package hash to not-yet-concrete specs, for which we know
            # we can compute the hash.
            if not spec.concrete:
                # we need force=True here because package hash assignment has to happen
                # before we mark concrete, so that we know what was *already* concrete.
                spec._cached_hash(ht.package_hash, force=True)

                # keep this check here to ensure package hash is saved
                assert getattr(spec, ht.package_hash.attr)

        # Mark everything in the spec as concrete
        self._mark_concrete()

        # Assign dag_hash (this *could* be done lazily, but it's assigned anyway in
        # ensure_no_deprecated, and it's clearer to see explicitly where it happens).
        # Any specs that were concrete before finalization will already have a cached
        # DAG hash.
        for spec in self.traverse():
            spec._cached_hash(ht.dag_hash)

    def concretized(self, tests=False):
        """This is a non-destructive version of concretize().

        First clones, then returns a concrete version of this package
        without modifying this package.

        Args:
            tests (bool or list): if False disregard 'test' dependencies,
                if a list of names activate them for the packages in the list,
                if True activate 'test' dependencies for all packages.
        """
        clone = self.copy()
        clone.concretize(tests=tests)
        return clone

    def flat_dependencies(self, disconnect: bool = False):
        """Build DependencyMap of all of this spec's dependencies with their constraints merged.

        Arguments:
            disconnect: if True, disconnect all dependents and dependencies among nodes in this
                spec's DAG.
        """
        flat_deps = {}
        deptree = self.traverse(root=False)

        for spec in deptree:
            if spec.name not in flat_deps:
                flat_deps[spec.name] = spec
            else:
                try:
                    flat_deps[spec.name].constrain(spec)
                except spack.error.UnsatisfiableSpecError as e:
                    # DAG contains two instances of the same package with inconsistent constraints.
                    raise InconsistentSpecError("Invalid Spec DAG: %s" % e.message) from e

        if disconnect:
            for spec in flat_deps.values():
                if not spec.concrete:
                    spec.clear_edges()
            self.clear_dependencies()

        return flat_deps

    def index(self, deptype="all"):
        """Return a dictionary that points to all the dependencies in this
        spec.
        """
        dm = collections.defaultdict(list)
        for spec in self.traverse(deptype=deptype):
            dm[spec.name].append(spec)
        return dm

    def _evaluate_dependency_conditions(self, name):
        """Evaluate all the conditions on a dependency with this name.

        Args:
            name (str): name of dependency to evaluate conditions on.

        Returns:
            (Dependency): new Dependency object combining all constraints.

        If the package depends on <name> in the current spec
        configuration, return the constrained dependency and
        corresponding dependency types.

        If no conditions are True (and we don't depend on it), return
        ``(None, None)``.
        """
        vt.substitute_abstract_variants(self)
        # evaluate when specs to figure out constraints on the dependency.
        dep = None
        for when_spec, deps_by_name in self.package_class.dependencies.items():
            if not self.satisfies(when_spec):
                continue

            for dep_name, dependency in deps_by_name.items():
                if dep_name != name:
                    continue

                if dep is None:
                    dep = dp.Dependency(Spec(self.name), Spec(name), depflag=0)
                try:
                    dep.merge(dependency)
                except spack.error.UnsatisfiableSpecError as e:
                    e.message = (
                        "Conflicting conditional dependencies for spec"
                        "\n\n\t{0}\n\n"
                        "Cannot merge constraint"
                        "\n\n\t{1}\n\n"
                        "into"
                        "\n\n\t{2}".format(self, dependency.spec, dep.spec)
                    )
                    raise e

        return dep

    def _find_provider(self, vdep, provider_index):
        """Find provider for a virtual spec in the provider index.
        Raise an exception if there is a conflicting virtual
        dependency already in this spec.
        """
        assert spack.repo.PATH.is_virtual_safe(vdep.name), vdep

        # note that this defensively copies.
        providers = provider_index.providers_for(vdep)

        # If there is a provider for the vpkg, then use that instead of
        # the virtual package.
        if providers:
            # Remove duplicate providers that can concretize to the same
            # result.
            for provider in providers:
                for spec in providers:
                    if spec is not provider and provider.intersects(spec):
                        providers.remove(spec)
            # Can't have multiple providers for the same thing in one spec.
            if len(providers) > 1:
                raise MultipleProviderError(vdep, providers)
            return providers[0]
        else:
            # The user might have required something insufficient for
            # pkg_dep -- so we'll get a conflict.  e.g., user asked for
            # mpi@:1.1 but some package required mpi@2.1:.
            required = provider_index.providers_for(vdep.name)
            if len(required) > 1:
                raise MultipleProviderError(vdep, required)
            elif required:
                raise UnsatisfiableProviderSpecError(required[0], vdep)

    def _merge_dependency(self, dependency, visited, spec_deps, provider_index, tests):
        """Merge dependency information from a Package into this Spec.

        Args:
            dependency (Dependency): dependency metadata from a package;
                this is typically the result of merging *all* matching
                dependency constraints from the package.
            visited (set): set of dependency nodes already visited by
                ``normalize()``.
            spec_deps (dict): ``dict`` of all dependencies from the spec
                being normalized.
            provider_index (dict): ``provider_index`` of virtual dep
                providers in the ``Spec`` as normalized so far.

        NOTE: Caller should assume that this routine owns the
        ``dependency`` parameter, i.e., it needs to be a copy of any
        internal structures.

        This is the core of ``normalize()``.  There are some basic steps:

          * If dep is virtual, evaluate whether it corresponds to an
            existing concrete dependency, and merge if so.

          * If it's real and it provides some virtual dep, see if it provides
            what some virtual dependency wants and merge if so.

          * Finally, if none of the above, merge dependency and its
            constraints into this spec.

        This method returns True if the spec was changed, False otherwise.

        """
        changed = False
        dep = dependency.spec

        # If it's a virtual dependency, try to find an existing
        # provider in the spec, and merge that.
        virtuals = ()
        if spack.repo.PATH.is_virtual_safe(dep.name):
            virtuals = (dep.name,)
            visited.add(dep.name)
            provider = self._find_provider(dep, provider_index)
            if provider:
                dep = provider
        else:
            index = spack.provider_index.ProviderIndex(
                repository=spack.repo.PATH, specs=[dep], restrict=True
            )
            items = list(spec_deps.items())
            for name, vspec in items:
                if not spack.repo.PATH.is_virtual_safe(vspec.name):
                    continue

                if index.providers_for(vspec):
                    vspec._replace_with(dep)
                    del spec_deps[vspec.name]
                    changed = True
                else:
                    required = index.providers_for(vspec.name)
                    if required:
                        raise UnsatisfiableProviderSpecError(required[0], dep)
            provider_index.update(dep)

        # If the spec isn't already in the set of dependencies, add it.
        # Note: dep is always owned by this method. If it's from the
        # caller, it's a copy from _evaluate_dependency_conditions. If it
        # comes from a vdep, it's a defensive copy from _find_provider.
        if dep.name not in spec_deps:
            if self.concrete:
                return False

            spec_deps[dep.name] = dep
            changed = True
        else:
            # merge package/vdep information into spec
            try:
                tty.debug("{0} applying constraint {1}".format(self.name, str(dep)))
                changed |= spec_deps[dep.name].constrain(dep)
            except spack.error.UnsatisfiableSpecError as e:
                fmt = "An unsatisfiable {0}".format(e.constraint_type)
                fmt += " constraint has been detected for spec:"
                fmt += "\n\n{0}\n\n".format(spec_deps[dep.name].tree(indent=4))
                fmt += "while trying to concretize the partial spec:"
                fmt += "\n\n{0}\n\n".format(self.tree(indent=4))
                fmt += "{0} requires {1} {2} {3}, but spec asked for {4}"

                e.message = fmt.format(
                    self.name, dep.name, e.constraint_type, e.required, e.provided
                )

                raise

        # Add merged spec to my deps and recurse
        spec_dependency = spec_deps[dep.name]
        if dep.name not in self._dependencies:
            self._add_dependency(spec_dependency, depflag=dependency.depflag, virtuals=virtuals)

        changed |= spec_dependency._normalize_helper(visited, spec_deps, provider_index, tests)
        return changed

    def _normalize_helper(self, visited, spec_deps, provider_index, tests):
        """Recursive helper function for _normalize."""
        if self.name in visited:
            return False
        visited.add(self.name)

        # If we descend into a virtual spec, there's nothing more
        # to normalize.  Concretize will finish resolving it later.
        if self.virtual or self.external:
            return False

        # Avoid recursively adding constraints for already-installed packages:
        # these may include build dependencies which are not needed for this
        # install (since this package is already installed).
        if self.concrete and self.installed:
            return False

        # Combine constraints from package deps with constraints from
        # the spec, until nothing changes.
        any_change = False
        changed = True

        while changed:
            changed = False
            for dep_name in self.package_class.dependency_names():
                # Do we depend on dep_name?  If so pkg_dep is not None.
                dep = self._evaluate_dependency_conditions(dep_name)

                # If dep is a needed dependency, merge it.
                if dep:
                    merge = (
                        # caller requested test dependencies
                        tests is True
                        or (tests and self.name in tests)
                        or
                        # this is not a test-only dependency
                        (dep.depflag & ~dt.TEST)
                    )

                    if merge:
                        changed |= self._merge_dependency(
                            dep, visited, spec_deps, provider_index, tests
                        )
            any_change |= changed

        return any_change

    def normalize(self, force=False, tests=False, user_spec_deps=None, disconnect=True):
        """When specs are parsed, any dependencies specified are hanging off
        the root, and ONLY the ones that were explicitly provided are there.
        Normalization turns a partial flat spec into a DAG, where:

        1. Known dependencies of the root package are in the DAG.
        2. Each node's dependencies dict only contains its known direct
           deps.
        3. There is only ONE unique spec for each package in the DAG.

           * This includes virtual packages.  If there a non-virtual
             package that provides a virtual package that is in the spec,
             then we replace the virtual package with the non-virtual one.

        TODO: normalize should probably implement some form of cycle
        detection, to ensure that the spec is actually a DAG.
        """
        if not self.name:
            raise spack.error.SpecError("Attempting to normalize anonymous spec")

        # Set _normal and _concrete to False when forced
        if force and not self._concrete:
            self._normal = False

        if self._normal:
            return False

        # Ensure first that all packages & compilers in the DAG exist.
        self.validate_or_raise()
        # Clear the DAG and collect all dependencies in the DAG, which will be
        # reapplied as constraints. All dependencies collected this way will
        # have been created by a previous execution of 'normalize'.
        # A dependency extracted here will only be reintegrated if it is
        # discovered to apply according to _normalize_helper, so
        # user-specified dependencies are recorded separately in case they
        # refer to specs which take several normalization passes to
        # materialize.
        all_spec_deps = self.flat_dependencies(disconnect=disconnect)

        if user_spec_deps:
            for name, spec in user_spec_deps.items():
                if not name:
                    msg = "Attempted to normalize anonymous dependency spec"
                    msg += " %s" % spec
                    raise InvalidSpecDetected(msg)
                if name not in all_spec_deps:
                    all_spec_deps[name] = spec
                else:
                    all_spec_deps[name].constrain(spec)

        # Initialize index of virtual dependency providers if
        # concretize didn't pass us one already
        provider_index = spack.provider_index.ProviderIndex(
            repository=spack.repo.PATH, specs=[s for s in all_spec_deps.values()], restrict=True
        )

        # traverse the package DAG and fill out dependencies according
        # to package files & their 'when' specs
        visited = set()

        any_change = self._normalize_helper(visited, all_spec_deps, provider_index, tests)

        # remove any leftover dependents outside the spec from, e.g., pruning externals
        valid = {id(spec) for spec in all_spec_deps.values()} | {id(self)}
        for spec in all_spec_deps.values():
            remove = [dep for dep in spec.dependents() if id(dep) not in valid]
            for dep in remove:
                del spec._dependents.edges[dep.name]
                del dep._dependencies.edges[spec.name]

        # Mark the spec as normal once done.
        self._normal = True
        return any_change

    def normalized(self):
        """
        Return a normalized copy of this spec without modifying this spec.
        """
        clone = self.copy()
        clone.normalize()
        return clone

    def validate_or_raise(self):
        """Checks that names and values in this spec are real. If they're not,
        it will raise an appropriate exception.
        """
        # FIXME: this function should be lazy, and collect all the errors
        # FIXME: before raising the exceptions, instead of being greedy and
        # FIXME: raise just the first one encountered
        for spec in self.traverse():
            # raise an UnknownPackageError if the spec's package isn't real.
            if (not spec.virtual) and spec.name:
                spack.repo.PATH.get_pkg_class(spec.fullname)

            # validate compiler in addition to the package name.
            if spec.compiler:
                if not spack.compilers.supported(spec.compiler):
                    raise UnsupportedCompilerError(spec.compiler.name)

            # Ensure correctness of variants (if the spec is not virtual)
            if not spec.virtual:
                Spec.ensure_valid_variants(spec)
                vt.substitute_abstract_variants(spec)

    @staticmethod
    def ensure_valid_variants(spec):
        """Ensures that the variant attached to a spec are valid.

        Args:
            spec (Spec): spec to be analyzed

        Raises:
            spack.variant.UnknownVariantError: on the first unknown variant found
        """
        # concrete variants are always valid
        if spec.concrete:
            return

        pkg_cls = spec.package_class
        pkg_variants = pkg_cls.variants
        # reserved names are variants that may be set on any package
        # but are not necessarily recorded by the package's class
        not_existing = set(spec.variants) - (
            set(pkg_variants) | set(spack.directives.reserved_names)
        )
        if not_existing:
            raise vt.UnknownVariantError(spec, not_existing)

    def update_variant_validate(self, variant_name, values):
        """If it is not already there, adds the variant named
        `variant_name` to the spec `spec` based on the definition
        contained in the package metadata. Validates the variant and
        values before returning.

        Used to add values to a variant without being sensitive to the
        variant being single or multi-valued. If the variant already
        exists on the spec it is assumed to be multi-valued and the
        values are appended.

        Args:
           variant_name: the name of the variant to add or append to
           values: the value or values (as a tuple) to add/append
                   to the variant
        """
        if not isinstance(values, tuple):
            values = (values,)

        pkg_variant, _ = self.package_class.variants[variant_name]

        for value in values:
            if self.variants.get(variant_name):
                msg = (
                    f"cannot append the new value '{value}' to the single-valued "
                    f"variant '{self.variants[variant_name]}'"
                )
                assert pkg_variant.multi, msg
                self.variants[variant_name].append(value)
            else:
                variant = pkg_variant.make_variant(value)
                self.variants[variant_name] = variant

        pkg_cls = spack.repo.PATH.get_pkg_class(self.name)
        pkg_variant.validate_or_raise(self.variants[variant_name], pkg_cls)

    def constrain(self, other, deps=True):
        """Intersect self with other in-place. Return True if self changed, False otherwise.

        Args:
            other: constraint to be added to self
            deps: if False, constrain only the root node, otherwise constrain dependencies
                as well.

        Raises:
             spack.error.UnsatisfiableSpecError: when self cannot be constrained
        """
        # If we are trying to constrain a concrete spec, either the spec
        # already satisfies the constraint (and the method returns False)
        # or it raises an exception
        if self.concrete:
            if self.satisfies(other):
                return False
            else:
                raise spack.error.UnsatisfiableSpecError(self, other, "constrain a concrete spec")

        other = self._autospec(other)
        if other.abstract_hash:
            if not self.abstract_hash or other.abstract_hash.startswith(self.abstract_hash):
                self.abstract_hash = other.abstract_hash
            elif not self.abstract_hash.startswith(other.abstract_hash):
                raise InvalidHashError(self, other.abstract_hash)

        if not (self.name == other.name or (not self.name) or (not other.name)):
            raise UnsatisfiableSpecNameError(self.name, other.name)

        if (
            other.namespace is not None
            and self.namespace is not None
            and other.namespace != self.namespace
        ):
            raise UnsatisfiableSpecNameError(self.fullname, other.fullname)

        if not self.versions.overlaps(other.versions):
            raise UnsatisfiableVersionSpecError(self.versions, other.versions)

        for v in [x for x in other.variants if x in self.variants]:
            if not self.variants[v].compatible(other.variants[v]):
                raise vt.UnsatisfiableVariantSpecError(self.variants[v], other.variants[v])

        # TODO: Check out the logic here
        sarch, oarch = self.architecture, other.architecture
        if sarch is not None and oarch is not None:
            if sarch.platform is not None and oarch.platform is not None:
                if sarch.platform != oarch.platform:
                    raise UnsatisfiableArchitectureSpecError(sarch, oarch)
            if sarch.os is not None and oarch.os is not None:
                if sarch.os != oarch.os:
                    raise UnsatisfiableArchitectureSpecError(sarch, oarch)
            if sarch.target is not None and oarch.target is not None:
                if sarch.target != oarch.target:
                    raise UnsatisfiableArchitectureSpecError(sarch, oarch)

        changed = False

        if not self.name and other.name:
            self.name = other.name
            changed = True

        if not self.namespace and other.namespace:
            self.namespace = other.namespace
            changed = True

        if self.compiler is not None and other.compiler is not None:
            changed |= self.compiler.constrain(other.compiler)
        elif self.compiler is None:
            changed |= self.compiler != other.compiler
            self.compiler = other.compiler

        changed |= self.versions.intersect(other.versions)
        changed |= self.variants.constrain(other.variants)

        changed |= self.compiler_flags.constrain(other.compiler_flags)

        old = str(self.architecture)
        sarch, oarch = self.architecture, other.architecture
        if sarch is None or other.architecture is None:
            self.architecture = sarch or oarch
        else:
            if sarch.platform is None or oarch.platform is None:
                self.architecture.platform = sarch.platform or oarch.platform
            if sarch.os is None or oarch.os is None:
                sarch.os = sarch.os or oarch.os
            if sarch.target is None or oarch.target is None:
                sarch.target = sarch.target or oarch.target
        changed |= str(self.architecture) != old

        if deps:
            changed |= self._constrain_dependencies(other)

        if other.concrete and not self.concrete and other.satisfies(self):
            self._finalize_concretization()

        return changed

    def _constrain_dependencies(self, other):
        """Apply constraints of other spec's dependencies to this spec."""
        other = self._autospec(other)

        if not other._dependencies:
            return False

        # TODO: might want more detail than this, e.g. specific deps
        # in violation. if this becomes a priority get rid of this
        # check and be more specific about what's wrong.
        if not other._intersects_dependencies(self):
            raise UnsatisfiableDependencySpecError(other, self)

        if any(not d.name for d in other.traverse(root=False)):
            raise UnconstrainableDependencySpecError(other)

        # Handle common first-order constraints directly
        changed = False
        for name in self.common_dependencies(other):
            changed |= self[name].constrain(other[name], deps=False)
            if name in self._dependencies:
                # WARNING: This function is an implementation detail of the
                # WARNING: original concretizer. Since with that greedy
                # WARNING: algorithm we don't allow multiple nodes from
                # WARNING: the same package in a DAG, here we hard-code
                # WARNING: using index 0 i.e. we assume that we have only
                # WARNING: one edge from package "name"
                edges_from_name = self._dependencies[name]
                changed |= edges_from_name[0].update_deptypes(other._dependencies[name][0].depflag)
                changed |= edges_from_name[0].update_virtuals(
                    other._dependencies[name][0].virtuals
                )

        # Update with additional constraints from other spec
        # operate on direct dependencies only, because a concrete dep
        # represented by hash may have structure that needs to be preserved
        for name in other.direct_dep_difference(self):
            dep_spec_copy = other._get_dependency(name)
            self._add_dependency(
                dep_spec_copy.spec.copy(),
                depflag=dep_spec_copy.depflag,
                virtuals=dep_spec_copy.virtuals,
            )
            changed = True

        return changed

    def common_dependencies(self, other):
        """Return names of dependencies that self an other have in common."""
        common = set(s.name for s in self.traverse(root=False))
        common.intersection_update(s.name for s in other.traverse(root=False))
        return common

    def constrained(self, other, deps=True):
        """Return a constrained copy without modifying this spec."""
        clone = self.copy(deps=deps)
        clone.constrain(other, deps)
        return clone

    def direct_dep_difference(self, other):
        """Returns dependencies in self that are not in other."""
        mine = set(dname for dname in self._dependencies)
        mine.difference_update(dname for dname in other._dependencies)
        return mine

    def _autospec(self, spec_like):
        """
        Used to convert arguments to specs.  If spec_like is a spec, returns
        it.  If it's a string, tries to parse a string.  If that fails, tries
        to parse a local spec from it (i.e. name is assumed to be self's name).
        """
        if isinstance(spec_like, Spec):
            return spec_like
        return Spec(spec_like)

    def intersects(self, other: Union[str, "Spec"], deps: bool = True) -> bool:
        """Return True if there exists at least one concrete spec that matches both
        self and other, otherwise False.

        This operation is commutative, and if two specs intersect it means that one
        can constrain the other.

        Args:
            other: spec to be checked for compatibility
            deps: if True check compatibility of dependency nodes too, if False only check root
        """
        other = self._autospec(other)

        if other.concrete and self.concrete:
            return self.dag_hash() == other.dag_hash()

        elif self.concrete:
            return self.satisfies(other)

        elif other.concrete:
            return other.satisfies(self)

        # From here we know both self and other are not concrete
        self_hash = self.abstract_hash
        other_hash = other.abstract_hash

        if (
            self_hash
            and other_hash
            and not (self_hash.startswith(other_hash) or other_hash.startswith(self_hash))
        ):
            return False

        # If the names are different, we need to consider virtuals
        if self.name != other.name and self.name and other.name:
            if self.virtual and other.virtual:
                # Two virtual specs intersect only if there are providers for both
                lhs = spack.repo.PATH.providers_for(str(self))
                rhs = spack.repo.PATH.providers_for(str(other))
                intersection = [s for s in lhs if any(s.intersects(z) for z in rhs)]
                return bool(intersection)

            # A provider can satisfy a virtual dependency.
            elif self.virtual or other.virtual:
                virtual_spec, non_virtual_spec = (self, other) if self.virtual else (other, self)
                try:
                    # Here we might get an abstract spec
                    pkg_cls = spack.repo.PATH.get_pkg_class(non_virtual_spec.fullname)
                    pkg = pkg_cls(non_virtual_spec)
                except spack.repo.UnknownEntityError:
                    # If we can't get package info on this spec, don't treat
                    # it as a provider of this vdep.
                    return False

                if pkg.provides(virtual_spec.name):
                    for when_spec, provided in pkg.provided.items():
                        if non_virtual_spec.intersects(when_spec, deps=False):
                            if any(vpkg.intersects(virtual_spec) for vpkg in provided):
                                return True
            return False

        # namespaces either match, or other doesn't require one.
        if (
            other.namespace is not None
            and self.namespace is not None
            and self.namespace != other.namespace
        ):
            return False

        if self.versions and other.versions:
            if not self.versions.intersects(other.versions):
                return False

        if self.compiler and other.compiler:
            if not self.compiler.intersects(other.compiler):
                return False

        if not self.variants.intersects(other.variants):
            return False

        if self.architecture and other.architecture:
            if not self.architecture.intersects(other.architecture):
                return False

        if not self.compiler_flags.intersects(other.compiler_flags):
            return False

        # If we need to descend into dependencies, do it, otherwise we're done.
        if deps:
            return self._intersects_dependencies(other)

        return True

    def _intersects_dependencies(self, other):
        if not other._dependencies or not self._dependencies:
            # one spec *could* eventually satisfy the other
            return True

        # Handle first-order constraints directly
        for name in self.common_dependencies(other):
            if not self[name].intersects(other[name], deps=False):
                return False

        # For virtual dependencies, we need to dig a little deeper.
        self_index = spack.provider_index.ProviderIndex(
            repository=spack.repo.PATH, specs=self.traverse(), restrict=True
        )
        other_index = spack.provider_index.ProviderIndex(
            repository=spack.repo.PATH, specs=other.traverse(), restrict=True
        )

        # These two loops handle cases where there is an overly restrictive
        # vpkg in one spec for a provider in the other (e.g., mpi@3: is not
        # compatible with mpich2)
        for spec in self.virtual_dependencies():
            if spec.name in other_index and not other_index.providers_for(spec):
                return False

        for spec in other.virtual_dependencies():
            if spec.name in self_index and not self_index.providers_for(spec):
                return False

        return True

    def satisfies(self, other: Union[str, "Spec"], deps: bool = True) -> bool:
        """Return True if all concrete specs matching self also match other, otherwise False.

        Args:
            other: spec to be satisfied
            deps: if True descend to dependencies, otherwise only check root node
        """
        other = self._autospec(other)

        if other.concrete:
            # The left-hand side must be the same singleton with identical hash. Notice that
            # package hashes can be different for otherwise indistinguishable concrete Spec
            # objects.
            return self.concrete and self.dag_hash() == other.dag_hash()

        # If the right-hand side has an abstract hash, make sure it's a prefix of the
        # left-hand side's (abstract) hash.
        if other.abstract_hash:
            compare_hash = self.dag_hash() if self.concrete else self.abstract_hash
            if not compare_hash or not compare_hash.startswith(other.abstract_hash):
                return False

        # If the names are different, we need to consider virtuals
        if self.name != other.name and self.name and other.name:
            # A concrete provider can satisfy a virtual dependency.
            if not self.virtual and other.virtual:
                try:
                    # Here we might get an abstract spec
                    pkg_cls = spack.repo.PATH.get_pkg_class(self.fullname)
                    pkg = pkg_cls(self)
                except spack.repo.UnknownEntityError:
                    # If we can't get package info on this spec, don't treat
                    # it as a provider of this vdep.
                    return False

                if pkg.provides(other.name):
                    for when_spec, provided in pkg.provided.items():
                        if self.satisfies(when_spec, deps=False):
                            if any(vpkg.intersects(other) for vpkg in provided):
                                return True
            return False

        # namespaces either match, or other doesn't require one.
        if (
            other.namespace is not None
            and self.namespace is not None
            and self.namespace != other.namespace
        ):
            return False

        if not self.versions.satisfies(other.versions):
            return False

        if self.compiler and other.compiler:
            if not self.compiler.satisfies(other.compiler):
                return False
        elif other.compiler and not self.compiler:
            return False

        if not self.variants.satisfies(other.variants):
            return False

        if self.architecture and other.architecture:
            if not self.architecture.satisfies(other.architecture):
                return False
        elif other.architecture and not self.architecture:
            return False

        if not self.compiler_flags.satisfies(other.compiler_flags):
            return False

        # If we need to descend into dependencies, do it, otherwise we're done.
        if not deps:
            return True

        # If there are no constraints to satisfy, we're done.
        if not other._dependencies:
            return True

        # If we have no dependencies, we can't satisfy any constraints.
        if not self._dependencies:
            return False

        # If we arrived here, the lhs root node satisfies the rhs root node. Now we need to check
        # all the edges that have an abstract parent, and verify that they match some edge in the
        # lhs.
        #
        # It might happen that the rhs brings in concrete sub-DAGs. For those we don't need to
        # verify the edge properties, cause everything is encoded in the hash of the nodes that
        # will be verified later.
        lhs_edges: Dict[str, Set[DependencySpec]] = collections.defaultdict(set)
        for rhs_edge in other.traverse_edges(root=False, cover="edges"):
            # If we are checking for ^mpi we need to verify if there is any edge
            if rhs_edge.spec.virtual:
                rhs_edge.update_virtuals(virtuals=(rhs_edge.spec.name,))

            if not rhs_edge.virtuals:
                continue

            # Skip edges from a concrete sub-DAG
            if rhs_edge.parent.concrete:
                continue

            if not lhs_edges:
                # Construct a map of the link/run subDAG + direct "build" edges,
                # keyed by dependency name
                for lhs_edge in self.traverse_edges(
                    root=False, cover="edges", deptype=("link", "run")
                ):
                    lhs_edges[lhs_edge.spec.name].add(lhs_edge)
                    for virtual_name in lhs_edge.virtuals:
                        lhs_edges[virtual_name].add(lhs_edge)

                build_edges = self.edges_to_dependencies(depflag=dt.BUILD)
                for lhs_edge in build_edges:
                    lhs_edges[lhs_edge.spec.name].add(lhs_edge)
                    for virtual_name in lhs_edge.virtuals:
                        lhs_edges[virtual_name].add(lhs_edge)

            # We don't have edges to this dependency
            current_dependency_name = rhs_edge.spec.name
            if current_dependency_name not in lhs_edges:
                return False

            for virtual in rhs_edge.virtuals:
                has_virtual = any(
                    virtual in edge.virtuals for edge in lhs_edges[current_dependency_name]
                )
                if not has_virtual:
                    return False

        # Edges have been checked above already, hence deps=False
        return all(
            any(lhs.satisfies(rhs, deps=False) for lhs in self.traverse(root=False))
            for rhs in other.traverse(root=False)
        )

    def virtual_dependencies(self):
        """Return list of any virtual deps in this spec."""
        return [spec for spec in self.traverse() if spec.virtual]

    @property  # type: ignore[misc] # decorated prop not supported in mypy
    def patches(self):
        """Return patch objects for any patch sha256 sums on this Spec.

        This is for use after concretization to iterate over any patches
        associated with this spec.

        TODO: this only checks in the package; it doesn't resurrect old
        patches from install directories, but it probably should.
        """
        if not hasattr(self, "_patches"):
            self._patches = []

            # translate patch sha256sums to patch objects by consulting the index
            if self._patches_assigned():
                for sha256 in self.variants["patches"]._patches_in_order_of_appearance:
                    index = spack.repo.PATH.patch_index
                    pkg_cls = spack.repo.PATH.get_pkg_class(self.name)
                    try:
                        patch = index.patch_for_package(sha256, pkg_cls)
                    except spack.patch.PatchLookupError as e:
                        raise spack.error.SpecError(
                            f"{e}. This usually means the patch was modified or removed. "
                            "To fix this, either reconcretize or use the original package "
                            "repository"
                        ) from e

                    self._patches.append(patch)

        return self._patches

    def _dup(self, other, deps: Union[bool, dt.DepTypes, dt.DepFlag] = True, cleardeps=True):
        """Copy the spec other into self.  This is an overwriting
        copy. It does not copy any dependents (parents), but by default
        copies dependencies.

        To duplicate an entire DAG, call _dup() on the root of the DAG.

        Args:
            other (Spec): spec to be copied onto ``self``
            deps: if True copies all the dependencies. If
                False copies None. If deptype/depflag, copy matching types.
            cleardeps (bool): if True clears the dependencies of ``self``,
                before possibly copying the dependencies of ``other`` onto
                ``self``

        Returns:
            True if ``self`` changed because of the copy operation,
            False otherwise.

        """
        # We don't count dependencies as changes here
        changed = True
        if hasattr(self, "name"):
            changed = (
                self.name != other.name
                and self.versions != other.versions
                and self.architecture != other.architecture
                and self.compiler != other.compiler
                and self.variants != other.variants
                and self._normal != other._normal
                and self.concrete != other.concrete
                and self.external_path != other.external_path
                and self.external_modules != other.external_modules
                and self.compiler_flags != other.compiler_flags
                and self.abstract_hash != other.abstract_hash
            )

        self._package = None

        # Local node attributes get copied first.
        self.name = other.name
        self.versions = other.versions.copy()
        self.architecture = other.architecture.copy() if other.architecture else None
        self.compiler = other.compiler.copy() if other.compiler else None
        if cleardeps:
            self._dependents = _EdgeMap(store_by=EdgeDirection.parent)
            self._dependencies = _EdgeMap(store_by=EdgeDirection.child)
        self.compiler_flags = other.compiler_flags.copy()
        self.compiler_flags.spec = self
        self.variants = other.variants.copy()
        self._build_spec = other._build_spec

        # FIXME: we manage _patches_in_order_of_appearance specially here
        # to keep it from leaking out of spec.py, but we should figure
        # out how to handle it more elegantly in the Variant classes.
        for k, v in other.variants.items():
            patches = getattr(v, "_patches_in_order_of_appearance", None)
            if patches:
                self.variants[k]._patches_in_order_of_appearance = patches

        self.variants.spec = self
        self.external_path = other.external_path
        self.external_modules = other.external_modules
        self.extra_attributes = other.extra_attributes
        self.namespace = other.namespace

        # If we copy dependencies, preserve DAG structure in the new spec
        if deps:
            # If caller restricted deptypes to be copied, adjust that here.
            # By default, just copy all deptypes
            depflag = dt.ALL
            if isinstance(deps, (tuple, list, str)):
                depflag = dt.canonicalize(deps)
            self._dup_deps(other, depflag)

        self._concrete = other._concrete

        self.abstract_hash = other.abstract_hash

        if self._concrete:
            self._dunder_hash = other._dunder_hash
            self._normal = other._normal
            for h in ht.hashes:
                setattr(self, h.attr, getattr(other, h.attr, None))
        else:
            self._dunder_hash = None
            # Note, we could use other._normal if we are copying all deps, but
            # always set it False here to avoid the complexity of checking
            self._normal = False
            for h in ht.hashes:
                setattr(self, h.attr, None)

        return changed

    def _dup_deps(self, other, depflag: dt.DepFlag):
        def spid(spec):
            return id(spec)

        new_specs = {spid(other): self}
        for edge in other.traverse_edges(cover="edges", root=False):
            if edge.depflag and not depflag & edge.depflag:
                continue

            if spid(edge.parent) not in new_specs:
                new_specs[spid(edge.parent)] = edge.parent.copy(deps=False)

            if spid(edge.spec) not in new_specs:
                new_specs[spid(edge.spec)] = edge.spec.copy(deps=False)

            new_specs[spid(edge.parent)].add_dependency_edge(
                new_specs[spid(edge.spec)], depflag=edge.depflag, virtuals=edge.virtuals
            )

    def copy(self, deps: Union[bool, dt.DepTypes, dt.DepFlag] = True, **kwargs):
        """Make a copy of this spec.

        Args:
            deps: Defaults to True. If boolean, controls
                whether dependencies are copied (copied if True). If a
                DepTypes or DepFlag is provided, *only* matching dependencies are copied.
            kwargs: additional arguments for internal use (passed to ``_dup``).

        Returns:
            A copy of this spec.

        Examples:
            Deep copy with dependencies::

                spec.copy()
                spec.copy(deps=True)

            Shallow copy (no dependencies)::

                spec.copy(deps=False)

            Only build and run dependencies::

                deps=('build', 'run'):

        """
        clone = Spec.__new__(Spec)
        clone._dup(self, deps=deps, **kwargs)
        return clone

    @property
    def version(self):
        if not self.versions.concrete:
            raise spack.error.SpecError("Spec version is not concrete: " + str(self))
        return self.versions[0]

    def __getitem__(self, name: str):
        """Get a dependency from the spec by its name. This call implicitly
        sets a query state in the package being retrieved. The behavior of
        packages may be influenced by additional query parameters that are
        passed after a colon symbol.

        Note that if a virtual package is queried a copy of the Spec is
        returned while for non-virtual a reference is returned.
        """
        query_parameters: List[str] = name.split(":")
        if len(query_parameters) > 2:
            raise KeyError("key has more than one ':' symbol. At most one is admitted.")

        name, query_parameters = query_parameters[0], query_parameters[1:]
        if query_parameters:
            # We have extra query parameters, which are comma separated
            # values
            csv = query_parameters.pop().strip()
            query_parameters = re.split(r"\s*,\s*", csv)

        order = lambda: itertools.chain(
            self.traverse_edges(deptype=dt.LINK, order="breadth", cover="edges"),
            self.edges_to_dependencies(depflag=dt.BUILD | dt.RUN | dt.TEST),
            self.traverse_edges(deptype=dt.ALL, order="breadth", cover="edges"),
        )

        # Consider runtime dependencies and direct build/test deps before transitive dependencies,
        # and prefer matches closest to the root.
        try:
            child: Spec = next(
                e.spec
                for e in itertools.chain(
                    (e for e in order() if e.spec.name == name or name in e.virtuals),
                    # for historical reasons
                    (e for e in order() if e.spec.concrete and e.spec.package.provides(name)),
                )
            )
        except StopIteration:
            raise KeyError(f"No spec with name {name} in {self}")

        if self._concrete:
            return SpecBuildInterface(child, name, query_parameters, _parent=self)

        return child

    def __contains__(self, spec):
        """True if this spec or some dependency satisfies the spec.

        Note: If ``spec`` is anonymous, we ONLY check whether the root
        satisfies it, NOT dependencies.  This is because most anonymous
        specs (e.g., ``@1.2``) don't make sense when applied across an
        entire DAG -- we limit them to the root.

        """
        spec = self._autospec(spec)

        # if anonymous or same name, we only have to look at the root
        if not spec.name or spec.name == self.name:
            return self.satisfies(spec)
        else:
            return any(s.satisfies(spec) for s in self.traverse(root=False))

    def eq_dag(self, other, deptypes=True, vs=None, vo=None):
        """True if the full dependency DAGs of specs are equal."""
        if vs is None:
            vs = set()
        if vo is None:
            vo = set()

        vs.add(id(self))
        vo.add(id(other))

        if not self.eq_node(other):
            return False

        if len(self._dependencies) != len(other._dependencies):
            return False

        ssorted = [self._dependencies[name] for name in sorted(self._dependencies)]
        osorted = [other._dependencies[name] for name in sorted(other._dependencies)]
        for s_dspec, o_dspec in zip(
            itertools.chain.from_iterable(ssorted), itertools.chain.from_iterable(osorted)
        ):
            if deptypes and s_dspec.depflag != o_dspec.depflag:
                return False

            s, o = s_dspec.spec, o_dspec.spec
            visited_s = id(s) in vs
            visited_o = id(o) in vo

            # Check for duplicate or non-equal dependencies
            if visited_s != visited_o:
                return False

            # Skip visited nodes
            if visited_s or visited_o:
                continue

            # Recursive check for equality
            if not s.eq_dag(o, deptypes, vs, vo):
                return False

        return True

    def _cmp_node(self):
        """Yield comparable elements of just *this node* and not its deps."""
        yield self.name
        yield self.namespace
        yield self.versions
        yield self.variants
        yield self.compiler
        yield self.compiler_flags
        yield self.architecture
        yield self.abstract_hash

        # this is not present on older specs
        yield getattr(self, "_package_hash", None)

    def eq_node(self, other):
        """Equality with another spec, not including dependencies."""
        return (other is not None) and lang.lazy_eq(self._cmp_node, other._cmp_node)

    def _cmp_iter(self):
        """Lazily yield components of self for comparison."""

        for item in self._cmp_node():
            yield item

        # This needs to be in _cmp_iter so that no specs with different process hashes
        # are considered the same by `__hash__` or `__eq__`.
        #
        # TODO: We should eventually unify the `_cmp_*` methods with `to_node_dict` so
        # TODO: there aren't two sources of truth, but this needs some thought, since
        # TODO: they exist for speed.  We should benchmark whether it's really worth
        # TODO: having two types of hashing now that we use `json` instead of `yaml` for
        # TODO: spec hashing.
        yield self.process_hash() if self.concrete else None

        def deps():
            for dep in sorted(itertools.chain.from_iterable(self._dependencies.values())):
                yield dep.spec.name
                yield dep.depflag
                yield hash(dep.spec)

        yield deps

    def format(self, format_string: str = DEFAULT_FORMAT, color: Optional[bool] = False) -> str:
        r"""Prints out particular pieces of a spec, depending on what is
        in the format string.

        Using the ``{attribute}`` syntax, any field of the spec can be
        selected.  Those attributes can be recursive. For example,
        ``s.format({compiler.version})`` will print the version of the
        compiler.

        Commonly used attributes of the Spec for format strings include::

            name
            version
            compiler
            compiler.name
            compiler.version
            compiler_flags
            variants
            architecture
            architecture.platform
            architecture.os
            architecture.target
            prefix

        Some additional special-case properties can be added::

            hash[:len]    The DAG hash with optional length argument
            spack_root    The spack root directory
            spack_install The spack install directory

        The ``^`` sigil can be used to access dependencies by name.
        ``s.format({^mpi.name})`` will print the name of the MPI
        implementation in the spec.

        The ``@``, ``%``, ``arch=``, and ``/`` sigils
        can be used to include the sigil with the printed
        string. These sigils may only be used with the appropriate
        attributes, listed below::

            @        ``{@version}``, ``{@compiler.version}``
            %        ``{%compiler}``, ``{%compiler.name}``
            arch=    ``{arch=architecture}``
            /        ``{/hash}``, ``{/hash:7}``, etc

        The ``@`` sigil may also be used for any other property named
        ``version``. Sigils printed with the attribute string are only
        printed if the attribute string is non-empty, and are colored
        according to the color of the attribute.

        Sigils are not used for printing variants. Variants listed by
        name naturally print with their sigil. For example,
        ``spec.format('{variants.debug}')`` would print either
        ``+debug`` or ``~debug`` depending on the name of the
        variant. Non-boolean variants print as ``name=value``. To
        print variant names or values independently, use
        ``spec.format('{variants.<name>.name}')`` or
        ``spec.format('{variants.<name>.value}')``.

        Spec format strings use ``\`` as the escape character. Use
        ``\{`` and ``\}`` for literal braces, and ``\\`` for the
        literal ``\`` character.

        Args:
            format_string: string containing the format to be expanded
            color: True for colorized result; False for no color; None for auto color.
        """
        ensure_modern_format_string(format_string)

        def safe_color(sigil: str, string: str, color_fmt: Optional[str]) -> str:
            # avoid colorizing if there is no color or the string is empty
            if (color is False) or not color_fmt or not string:
                return sigil + string
            # escape and add the sigil here to avoid multiple concatenations
            if sigil == "@":
                sigil = "@@"
            return clr.colorize(f"{color_fmt}{sigil}{clr.cescape(string)}@.", color=color)

        def format_attribute(match_object: Match) -> str:
            (esc, sig, dep, hash, hash_len, attribute, close_brace, unmatched_close_brace) = (
                match_object.groups()
            )
            if esc:
                return esc
            elif unmatched_close_brace:
                raise SpecFormatStringError(f"Unmatched close brace: '{format_string}'")
            elif not close_brace:
                raise SpecFormatStringError(f"Missing close brace: '{format_string}'")

            current = self if dep is None else self[dep]

            # Hash attributes can return early.
            # NOTE: we currently treat abstract_hash like an attribute and ignore
            # any length associated with it. We may want to change that.
            if hash:
                if sig and sig != "/":
                    raise SpecFormatSigilError(sig, "DAG hashes", hash)
                try:
                    length = int(hash_len) if hash_len else None
                except ValueError:
                    raise SpecFormatStringError(f"Invalid hash length: '{hash_len}'")
                return safe_color(sig or "", current.dag_hash(length), HASH_COLOR)

            if attribute == "":
                raise SpecFormatStringError("Format string attributes must be non-empty")

            attribute = attribute.lower()
            parts = attribute.split(".")
            assert parts

            # check that the sigil is valid for the attribute.
            if not sig:
                sig = ""
            elif sig == "@" and parts[-1] not in ("versions", "version"):
                raise SpecFormatSigilError(sig, "versions", attribute)
            elif sig == "%" and attribute not in ("compiler", "compiler.name"):
                raise SpecFormatSigilError(sig, "compilers", attribute)
            elif sig == "/" and attribute != "abstract_hash":
                raise SpecFormatSigilError(sig, "DAG hashes", attribute)
            elif sig == "arch=":
                if attribute not in ("architecture", "arch"):
                    raise SpecFormatSigilError(sig, "the architecture", attribute)
                sig = " arch="  # include space as separator

            # Iterate over components using getattr to get next element
            for idx, part in enumerate(parts):
                if not part:
                    raise SpecFormatStringError("Format string attributes must be non-empty")
                if part.startswith("_"):
                    raise SpecFormatStringError("Attempted to format private attribute")
                else:
                    if isinstance(current, vt.VariantMap):
                        # subscript instead of getattr for variant names
                        try:
                            current = current[part]
                        except KeyError:
                            raise SpecFormatStringError(f"Variant '{part}' does not exist")
                    else:
                        # aliases
                        if part == "arch":
                            part = "architecture"
                        elif part == "version":
                            # version (singular) requires a concrete versions list. Avoid
                            # pedantic errors by using versions (plural) when not concrete.
                            # These two are not entirely equivalent for pkg@=1.2.3:
                            # - version prints '1.2.3'
                            # - versions prints '=1.2.3'
                            if not current.versions.concrete:
                                part = "versions"
                        try:
                            current = getattr(current, part)
                        except AttributeError:
                            parent = ".".join(parts[:idx])
                            m = "Attempted to format attribute %s." % attribute
                            m += "Spec %s has no attribute %s" % (parent, part)
                            raise SpecFormatStringError(m)
                        if isinstance(current, vn.VersionList):
                            if current == vn.any_version:
                                # don't print empty version lists
                                return ""

                    if callable(current):
                        raise SpecFormatStringError("Attempted to format callable object")

                    if current is None:
                        # not printing anything
                        return ""

            # Set color codes for various attributes
            color = None
            if "variants" in parts:
                color = VARIANT_COLOR
            elif "architecture" in parts:
                color = ARCHITECTURE_COLOR
            elif "compiler" in parts or "compiler_flags" in parts:
                color = COMPILER_COLOR
            elif "version" in parts or "versions" in parts:
                color = VERSION_COLOR

            # return colored output
            return safe_color(sig, str(current), color)

        return SPEC_FORMAT_RE.sub(format_attribute, format_string).strip()

    def cformat(self, *args, **kwargs):
        """Same as format, but color defaults to auto instead of False."""
        kwargs = kwargs.copy()
        kwargs.setdefault("color", None)
        return self.format(*args, **kwargs)

    @property
    def spack_root(self):
        """Special field for using ``{spack_root}`` in Spec.format()."""
        return spack.paths.spack_root

    @property
    def spack_install(self):
        """Special field for using ``{spack_install}`` in Spec.format()."""
        return spack.store.STORE.layout.root

    def format_path(
        # self, format_string: str, _path_ctor: Optional[pathlib.PurePath] = None
        self,
        format_string: str,
        _path_ctor: Optional[Callable[[Any], pathlib.PurePath]] = None,
    ) -> str:
        """Given a `format_string` that is intended as a path, generate a string
        like from `Spec.format`, but eliminate extra path separators introduced by
        formatting of Spec properties.

        Path separators explicitly added to the string are preserved, so for example
        "{name}/{version}" would generate a directory based on the Spec's name, and
        a subdirectory based on its version; this function guarantees though that
        the resulting string would only have two directories (i.e. that if under
        normal circumstances that `str(Spec.version)` would contain a path
        separator, it would not in this case).
        """
        format_component_with_sep = r"\{[^}]*[/\\][^}]*}"
        if re.search(format_component_with_sep, format_string):
            raise SpecFormatPathError(
                f"Invalid path format string: cannot contain {{/...}}\n\t{format_string}"
            )

        path_ctor = _path_ctor or pathlib.PurePath
        format_string_as_path = path_ctor(format_string)
        if format_string_as_path.is_absolute() or (
            # Paths that begin with a single "\" on windows are relative, but we still
            # want to preserve the initial "\\" to be consistent with PureWindowsPath.
            # Ensure that this '\' is not passed to polite_filename() so it's not converted to '_'
            (os.name == "nt" or path_ctor == pathlib.PureWindowsPath)
            and format_string_as_path.parts[0] == "\\"
        ):
            output_path_components = [format_string_as_path.parts[0]]
            input_path_components = list(format_string_as_path.parts[1:])
        else:
            output_path_components = []
            input_path_components = list(format_string_as_path.parts)

        output_path_components += [
            fs.polite_filename(self.format(part)) for part in input_path_components
        ]
        return str(path_ctor(*output_path_components))

    def __str__(self):
        if not self._dependencies:
            return self.format()
        root_str = [self.format()]
        sorted_dependencies = sorted(
            self.traverse(root=False), key=lambda x: (x.name, x.abstract_hash)
        )
        sorted_dependencies = [
            d.format("{edge_attributes} " + DEFAULT_FORMAT) for d in sorted_dependencies
        ]
        spec_str = " ^".join(root_str + sorted_dependencies)
        return spec_str.strip()

    @property
    def colored_str(self):
        root_str = [self.cformat()]
        sorted_dependencies = sorted(
            self.traverse(root=False), key=lambda x: (x.name, x.abstract_hash)
        )
        sorted_dependencies = [
            d.cformat("{edge_attributes} " + DISPLAY_FORMAT) for d in sorted_dependencies
        ]
        spec_str = " ^".join(root_str + sorted_dependencies)
        return spec_str.strip()

    def install_status(self):
        """Helper for tree to print DB install status."""
        if not self.concrete:
            return InstallStatus.absent

        if self.external:
            return InstallStatus.external

        upstream, record = spack.store.STORE.db.query_by_spec_hash(self.dag_hash())
        if not record:
            return InstallStatus.absent
        elif upstream and record.installed:
            return InstallStatus.upstream
        elif record.installed:
            return InstallStatus.installed
        else:
            return InstallStatus.missing

    def _installed_explicitly(self):
        """Helper for tree to print DB install status."""
        if not self.concrete:
            return None
        try:
            record = spack.store.STORE.db.get_record(self)
            return record.explicit
        except KeyError:
            return None

    def tree(
        self,
        *,
        color: Optional[bool] = None,
        depth: bool = False,
        hashes: bool = False,
        hashlen: Optional[int] = None,
        cover: str = "nodes",
        indent: int = 0,
        format: str = DEFAULT_FORMAT,
        deptypes: Union[Tuple[str, ...], str] = "all",
        show_types: bool = False,
        depth_first: bool = False,
        recurse_dependencies: bool = True,
        status_fn: Optional[Callable[["Spec"], InstallStatus]] = None,
        prefix: Optional[Callable[["Spec"], str]] = None,
    ) -> str:
        """Prints out this spec and its dependencies, tree-formatted
        with indentation.

        Status function may either output a boolean or an InstallStatus

        Args:
            color: if True, always colorize the tree. If False, don't colorize the tree. If None,
                use the default from llnl.tty.color
            depth: print the depth from the root
            hashes: if True, print the hash of each node
            hashlen: length of the hash to be printed
            cover: either "nodes" or "edges"
            indent: extra indentation for the tree being printed
            format: format to be used to print each node
            deptypes: dependency types to be represented in the tree
            show_types: if True, show the (merged) dependency type of a node
            depth_first: if True, traverse the DAG depth first when representing it as a tree
            recurse_dependencies: if True, recurse on dependencies
            status_fn: optional callable that takes a node as an argument and return its
                installation status
            prefix: optional callable that takes a node as an argument and return its
                installation prefix
        """
        out = ""

        if color is None:
            color = clr.get_color_when()

        for d, dep_spec in traverse.traverse_tree(
            [self], cover=cover, deptype=deptypes, depth_first=depth_first
        ):
            node = dep_spec.spec

            if prefix is not None:
                out += prefix(node)
            out += " " * indent

            if depth:
                out += "%-4d" % d

            if status_fn:
                status = status_fn(node)
                if status in list(InstallStatus):
                    out += clr.colorize(status.value, color=color)
                elif status:
                    out += clr.colorize("@g{[+]}  ", color=color)
                else:
                    out += clr.colorize("@r{[-]}  ", color=color)

            if hashes:
                out += clr.colorize("@K{%s}  ", color=color) % node.dag_hash(hashlen)

            if show_types:
                if cover == "nodes":
                    # when only covering nodes, we merge dependency types
                    # from all dependents before showing them.
                    depflag = 0
                    for ds in node.edges_from_dependents():
                        depflag |= ds.depflag
                else:
                    # when covering edges or paths, we show dependency
                    # types only for the edge through which we visited
                    depflag = dep_spec.depflag

                type_chars = dt.flag_to_chars(depflag)
                out += "[%s]  " % type_chars

            out += "    " * d
            if d > 0:
                out += "^"
            out += node.format(format, color=color) + "\n"

            # Check if we wanted just the first line
            if not recurse_dependencies:
                break

        return out

    def __repr__(self):
        return str(self)

    @property
    def platform(self):
        return self.architecture.platform

    @property
    def os(self):
        return self.architecture.os

    @property
    def target(self):
        # This property returns the underlying microarchitecture object
        # to give to the attribute the appropriate comparison semantic
        return self.architecture.target.microarchitecture

    @property
    def build_spec(self):
        return self._build_spec or self

    @build_spec.setter
    def build_spec(self, value):
        self._build_spec = value

    def trim(self, dep_name):
        """
        Remove any package that is or provides `dep_name` transitively
        from this tree. This can also remove other dependencies if
        they are only present because of `dep_name`.
        """
        for spec in list(self.traverse()):
            new_dependencies = _EdgeMap()  # A new _EdgeMap
            for pkg_name, edge_list in spec._dependencies.items():
                for edge in edge_list:
                    if (dep_name not in edge.virtuals) and (not dep_name == edge.spec.name):
                        new_dependencies.add(edge)
            spec._dependencies = new_dependencies

    def splice(self, other, transitive):
        """Splices dependency "other" into this ("target") Spec, and return the
        result as a concrete Spec.
        If transitive, then other and its dependencies will be extrapolated to
        a list of Specs and spliced in accordingly.
        For example, let there exist a dependency graph as follows:
        T
        | \
        Z<-H
        In this example, Spec T depends on H and Z, and H also depends on Z.
        Suppose, however, that we wish to use a different H, known as H'. This
        function will splice in the new H' in one of two ways:
        1. transitively, where H' depends on the Z' it was built with, and the
        new T* also directly depends on this new Z', or
        2. intransitively, where the new T* and H' both depend on the original
        Z.
        Since the Spec returned by this splicing function is no longer deployed
        the same way it was built, any such changes are tracked by setting the
        build_spec to point to the corresponding dependency from the original
        Spec.
        TODO: Extend this for non-concrete Specs.
        """
        assert self.concrete
        assert other.concrete

        virtuals_to_replace = [v.name for v in other.package.virtuals_provided if v in self]
        if virtuals_to_replace:
            deps_to_replace = dict((self[v], other) for v in virtuals_to_replace)
            # deps_to_replace = [self[v] for v in virtuals_to_replace]
        else:
            # TODO: sanity check and error raise here for other.name not in self
            deps_to_replace = {self[other.name]: other}
            # deps_to_replace = [self[other.name]]

        for d in deps_to_replace:
            if not all(
                v in other.package.virtuals_provided or v not in self
                for v in d.package.virtuals_provided
            ):
                # There was something provided by the original that we don't
                # get from its replacement.
                raise SpliceError(
                    ("Splice between {0} and {1} will not provide " "the same virtuals.").format(
                        self.name, other.name
                    )
                )
            for n in d.traverse(root=False):
                if not all(
                    any(
                        v in other_n.package.virtuals_provided
                        for other_n in other.traverse(root=False)
                    )
                    or v not in self
                    for v in n.package.virtuals_provided
                ):
                    raise SpliceError(
                        (
                            "Splice between {0} and {1} will not provide " "the same virtuals."
                        ).format(self.name, other.name)
                    )

        # For now, check that we don't have DAG with multiple specs from the
        # same package
        def multiple_specs(root):
            counter = collections.Counter([node.name for node in root.traverse()])
            _, max_number = counter.most_common()[0]
            return max_number > 1

        if multiple_specs(self) or multiple_specs(other):
            msg = (
                'Either "{0}" or "{1}" contain multiple specs from the same '
                "package, which cannot be handled by splicing at the moment"
            )
            raise ValueError(msg.format(self, other))

        # Multiple unique specs with the same name will collide, so the
        # _dependents of these specs should not be trusted.
        # Variants may also be ignored here for now...

        # Keep all cached hashes because we will invalidate the ones that need
        # invalidating later, and we don't want to invalidate unnecessarily

        def from_self(name, transitive):
            if transitive:
                if name in other:
                    return False
                if any(v in other for v in self[name].package.virtuals_provided):
                    return False
                return True
            else:
                if name == other.name:
                    return False
                if any(
                    v in other.package.virtuals_provided
                    for v in self[name].package.virtuals_provided
                ):
                    return False
                return True

        self_nodes = dict(
            (s.name, s.copy(deps=False))
            for s in self.traverse(root=True)
            if from_self(s.name, transitive)
        )

        if transitive:
            other_nodes = dict((s.name, s.copy(deps=False)) for s in other.traverse(root=True))
        else:
            # NOTE: Does not fully validate providers; loader races possible
            other_nodes = dict(
                (s.name, s.copy(deps=False))
                for s in other.traverse(root=True)
                if s is other or s.name not in self
            )

        nodes = other_nodes.copy()
        nodes.update(self_nodes)

        for name in nodes:
            if name in self_nodes:
                for edge in self[name].edges_to_dependencies():
                    dep_name = deps_to_replace.get(edge.spec, edge.spec).name
                    nodes[name].add_dependency_edge(
                        nodes[dep_name], depflag=edge.depflag, virtuals=edge.virtuals
                    )
                if any(dep not in self_nodes for dep in self[name]._dependencies):
                    nodes[name].build_spec = self[name].build_spec
            else:
                for edge in other[name].edges_to_dependencies():
                    nodes[name].add_dependency_edge(
                        nodes[edge.spec.name], depflag=edge.depflag, virtuals=edge.virtuals
                    )
                if any(dep not in other_nodes for dep in other[name]._dependencies):
                    nodes[name].build_spec = other[name].build_spec

        ret = nodes[self.name]

        # Clear cached hashes for all affected nodes
        # Do not touch unaffected nodes
        for dep in ret.traverse(root=True, order="post"):
            opposite = other_nodes if dep.name in self_nodes else self_nodes
            if any(name in dep for name in opposite.keys()):
                # package hash cannot be affected by splice
                dep.clear_cached_hashes(ignore=["package_hash"])

                dep.dag_hash()

        return nodes[self.name]

    def clear_cached_hashes(self, ignore=()):
        """
        Clears all cached hashes in a Spec, while preserving other properties.
        """
        for h in ht.hashes:
            if h.attr not in ignore:
                if hasattr(self, h.attr):
                    setattr(self, h.attr, None)
        self._dunder_hash = None

    def __hash__(self):
        # If the spec is concrete, we leverage the process hash and just use
        # a 64-bit prefix of it. The process hash has the advantage that it's
        # computed once per concrete spec, and it's saved -- so if we read
        # concrete specs we don't need to recompute the whole hash. This is
        # good for large, unchanging specs.
        #
        # We use the process hash instead of the DAG hash here because the DAG
        # hash includes the package hash, which can cause infinite recursion,
        # and which isn't defined unless the spec has a known package.
        if self.concrete:
            if not self._dunder_hash:
                self._dunder_hash = self.process_hash_bit_prefix(64)
            return self._dunder_hash

        # This is the normal hash for lazy_lexicographic_ordering. It's
        # slow for large specs because it traverses the whole spec graph,
        # so we hope it only runs on abstract specs, which are small.
        return hash(lang.tuplify(self._cmp_iter))

    def __reduce__(self):
        return Spec.from_dict, (self.to_dict(hash=ht.process_hash),)

    def attach_git_version_lookup(self):
        # Add a git lookup method for GitVersions
        if not self.name:
            return
        for v in self.versions:
            if isinstance(v, vn.GitVersion) and v._ref_version is None:
                v.attach_lookup(spack.version.git_ref_lookup.GitRefLookup(self.fullname))


def parse_with_version_concrete(string: str, compiler: bool = False):
    """Same as Spec(string), but interprets @x as @=x"""
    s: Union[CompilerSpec, Spec] = CompilerSpec(string) if compiler else Spec(string)
    interpreted_version = s.versions.concrete_range_as_version
    if interpreted_version:
        s.versions = vn.VersionList([interpreted_version])
    return s


def merge_abstract_anonymous_specs(*abstract_specs: Spec):
    """Merge the abstracts specs passed as input and return the result.

    The root specs must be anonymous, and it's duty of the caller to ensure that.

    This function merge the abstract specs based on package names. In particular
    it doesn't try to resolve virtual dependencies.

    Args:
        *abstract_specs: abstract specs to be merged
    """
    merged_spec = spack.spec.Spec()
    for current_spec_constraint in abstract_specs:
        merged_spec.constrain(current_spec_constraint, deps=False)

        for name in merged_spec.common_dependencies(current_spec_constraint):
            merged_spec[name].constrain(current_spec_constraint[name], deps=False)

        # Update with additional constraints from other spec
        for name in current_spec_constraint.direct_dep_difference(merged_spec):
            edge = next(iter(current_spec_constraint.edges_to_dependencies(name)))

            merged_spec._add_dependency(
                edge.spec.copy(), depflag=edge.depflag, virtuals=edge.virtuals
            )

    return merged_spec


def reconstruct_virtuals_on_edges(spec):
    """Reconstruct virtuals on edges. Used to read from old DB and reindex.

    Args:
        spec: spec on which we want to reconstruct virtuals
    """
    # Collect all possible virtuals
    possible_virtuals = set()
    for node in spec.traverse():
        try:
            possible_virtuals.update({x for x in node.package.dependencies if Spec(x).virtual})
        except Exception as e:
            warnings.warn(f"cannot reconstruct virtual dependencies on package {node.name}: {e}")
            continue

    # Assume all incoming edges to provider are marked with virtuals=
    for vspec in possible_virtuals:
        try:
            provider = spec[vspec]
        except KeyError:
            # Virtual not in the DAG
            continue

        for edge in provider.edges_from_dependents():
            edge.update_virtuals([vspec])


class SpecfileReaderBase:
    @classmethod
    def from_node_dict(cls, node):
        spec = Spec()

        name, node = cls.name_and_data(node)
        for h in ht.hashes:
            setattr(spec, h.attr, node.get(h.name, None))

        spec.name = name
        spec.namespace = node.get("namespace", None)

        if "version" in node or "versions" in node:
            spec.versions = vn.VersionList.from_dict(node)
            spec.attach_git_version_lookup()

        if "arch" in node:
            spec.architecture = ArchSpec.from_dict(node)

        if "compiler" in node:
            spec.compiler = CompilerSpec.from_dict(node)
        else:
            spec.compiler = None

        propagated_names = node.get("propagate", [])
        for name, values in node.get("parameters", {}).items():
            propagate = name in propagated_names
            if name in _valid_compiler_flags:
                spec.compiler_flags[name] = []
                for val in values:
                    spec.compiler_flags.add_flag(name, val, propagate)
            else:
                spec.variants[name] = vt.MultiValuedVariant.from_node_dict(
                    name, values, propagate=propagate
                )

        spec.external_path = None
        spec.external_modules = None
        if "external" in node:
            # This conditional is needed because sometimes this function is
            # called with a node already constructed that contains a 'versions'
            # and 'external' field. Related to virtual packages provider
            # indexes.
            if node["external"]:
                spec.external_path = node["external"]["path"]
                spec.external_modules = node["external"]["module"]
                if spec.external_modules is False:
                    spec.external_modules = None
                spec.extra_attributes = node["external"].get(
                    "extra_attributes", syaml.syaml_dict()
                )

        # specs read in are concrete unless marked abstract
        if node.get("concrete", True):
            spec._mark_root_concrete()

        if "patches" in node:
            patches = node["patches"]
            if len(patches) > 0:
                mvar = spec.variants.setdefault("patches", vt.MultiValuedVariant("patches", ()))
                mvar.value = patches
                # FIXME: Monkey patches mvar to store patches order
                mvar._patches_in_order_of_appearance = patches

        # Don't read dependencies here; from_dict() is used by
        # from_yaml() and from_json() to read the root *and* each dependency
        # spec.

        return spec

    @classmethod
    def _load(cls, data):
        """Construct a spec from JSON/YAML using the format version 2.

        This format is used in Spack v0.17, was introduced in
        https://github.com/spack/spack/pull/22845

        Args:
            data: a nested dict/list data structure read from YAML or JSON.
        """
        # Current specfile format
        nodes = data["spec"]["nodes"]
        hash_type = None
        any_deps = False

        # Pass 0: Determine hash type
        for node in nodes:
            for _, _, _, dhash_type, _ in cls.dependencies_from_node_dict(node):
                any_deps = True
                if dhash_type:
                    hash_type = dhash_type
                    break

        if not any_deps:  # If we never see a dependency...
            hash_type = ht.dag_hash.name
        elif not hash_type:  # Seen a dependency, still don't know hash_type
            raise spack.error.SpecError(
                "Spec dictionary contains malformed dependencies. Old format?"
            )

        hash_dict = {}
        root_spec_hash = None

        # Pass 1: Create a single lookup dictionary by hash
        for i, node in enumerate(nodes):
            node_hash = node[hash_type]
            node_spec = cls.from_node_dict(node)
            hash_dict[node_hash] = node
            hash_dict[node_hash]["node_spec"] = node_spec
            if i == 0:
                root_spec_hash = node_hash

        if not root_spec_hash:
            raise spack.error.SpecError("Spec dictionary contains no nodes.")

        # Pass 2: Finish construction of all DAG edges (including build specs)
        for node_hash, node in hash_dict.items():
            node_spec = node["node_spec"]
            for _, dhash, dtype, _, virtuals in cls.dependencies_from_node_dict(node):
                node_spec._add_dependency(
                    hash_dict[dhash]["node_spec"],
                    depflag=dt.canonicalize(dtype),
                    virtuals=virtuals,
                )
            if "build_spec" in node.keys():
                _, bhash, _ = cls.build_spec_from_node_dict(node, hash_type=hash_type)
                node_spec._build_spec = hash_dict[bhash]["node_spec"]

        return hash_dict[root_spec_hash]["node_spec"]


class SpecfileV1(SpecfileReaderBase):
    @classmethod
    def load(cls, data):
        """Construct a spec from JSON/YAML using the format version 1.

        Note: Version 1 format has no notion of a build_spec, and names are
        guaranteed to be unique. This function is guaranteed to read specs as
        old as v0.10 - while it was not checked for older formats.

        Args:
            data: a nested dict/list data structure read from YAML or JSON.
        """
        nodes = data["spec"]

        # Read nodes out of list.  Root spec is the first element;
        # dependencies are the following elements.
        dep_list = [cls.from_node_dict(node) for node in nodes]
        if not dep_list:
            raise spack.error.SpecError("specfile contains no nodes.")

        deps = {spec.name: spec for spec in dep_list}
        result = dep_list[0]

        for node in nodes:
            # get dependency dict from the node.
            name, data = cls.name_and_data(node)
            for dname, _, dtypes, _, virtuals in cls.dependencies_from_node_dict(data):
                deps[name]._add_dependency(
                    deps[dname], depflag=dt.canonicalize(dtypes), virtuals=virtuals
                )

        reconstruct_virtuals_on_edges(result)
        return result

    @classmethod
    def name_and_data(cls, node):
        name = next(iter(node))
        node = node[name]
        return name, node

    @classmethod
    def dependencies_from_node_dict(cls, node):
        if "dependencies" not in node:
            return []

        for t in cls.read_specfile_dep_specs(node["dependencies"]):
            yield t

    @classmethod
    def read_specfile_dep_specs(cls, deps, hash_type=ht.dag_hash.name):
        """Read the DependencySpec portion of a YAML-formatted Spec.
        This needs to be backward-compatible with older spack spec
        formats so that reindex will work on old specs/databases.
        """
        for dep_name, elt in deps.items():
            if isinstance(elt, dict):
                for h in ht.hashes:
                    if h.name in elt:
                        dep_hash, deptypes = elt[h.name], elt["type"]
                        hash_type = h.name
                        virtuals = []
                        break
                else:  # We never determined a hash type...
                    raise spack.error.SpecError("Couldn't parse dependency spec.")
            else:
                raise spack.error.SpecError("Couldn't parse dependency types in spec.")
            yield dep_name, dep_hash, list(deptypes), hash_type, list(virtuals)


class SpecfileV2(SpecfileReaderBase):
    @classmethod
    def load(cls, data):
        result = cls._load(data)
        reconstruct_virtuals_on_edges(result)
        return result

    @classmethod
    def name_and_data(cls, node):
        return node["name"], node

    @classmethod
    def dependencies_from_node_dict(cls, node):
        return cls.read_specfile_dep_specs(node.get("dependencies", []))

    @classmethod
    def read_specfile_dep_specs(cls, deps, hash_type=ht.dag_hash.name):
        """Read the DependencySpec portion of a YAML-formatted Spec.
        This needs to be backward-compatible with older spack spec
        formats so that reindex will work on old specs/databases.
        """
        if not isinstance(deps, list):
            raise spack.error.SpecError("Spec dictionary contains malformed dependencies")

        result = []
        for dep in deps:
            elt = dep
            dep_name = dep["name"]
            if isinstance(elt, dict):
                # new format: elements of dependency spec are keyed.
                for h in ht.hashes:
                    if h.name in elt:
                        dep_hash, deptypes, hash_type, virtuals = cls.extract_info_from_dep(elt, h)
                        break
                else:  # We never determined a hash type...
                    raise spack.error.SpecError("Couldn't parse dependency spec.")
            else:
                raise spack.error.SpecError("Couldn't parse dependency types in spec.")
            result.append((dep_name, dep_hash, list(deptypes), hash_type, list(virtuals)))
        return result

    @classmethod
    def extract_info_from_dep(cls, elt, hash):
        dep_hash, deptypes = elt[hash.name], elt["type"]
        hash_type = hash.name
        virtuals = []
        return dep_hash, deptypes, hash_type, virtuals

    @classmethod
    def build_spec_from_node_dict(cls, node, hash_type=ht.dag_hash.name):
        build_spec_dict = node["build_spec"]
        return build_spec_dict["name"], build_spec_dict[hash_type], hash_type


class SpecfileV3(SpecfileV2):
    pass


class SpecfileV4(SpecfileV2):
    @classmethod
    def extract_info_from_dep(cls, elt, hash):
        dep_hash = elt[hash.name]
        deptypes = elt["parameters"]["deptypes"]
        hash_type = hash.name
        virtuals = elt["parameters"]["virtuals"]
        return dep_hash, deptypes, hash_type, virtuals

    @classmethod
    def load(cls, data):
        return cls._load(data)


class LazySpecCache(collections.defaultdict):
    """Cache for Specs that uses a spec_like as key, and computes lazily
    the corresponding value ``Spec(spec_like``.
    """

    def __init__(self):
        super().__init__(Spec)

    def __missing__(self, key):
        value = self.default_factory(key)
        self[key] = value
        return value


def save_dependency_specfiles(root: Spec, output_directory: str, dependencies: List[Spec]):
    """Given a root spec (represented as a yaml object), index it with a subset
    of its dependencies, and write each dependency to a separate yaml file
    in the output directory.  By default, all dependencies will be written
    out.  To choose a smaller subset of dependencies to be written, pass a
    list of package names in the dependencies parameter. If the format of the
    incoming spec is not json, that can be specified with the spec_format
    parameter. This can be used to convert from yaml specfiles to the
    json format."""

    for spec in root.traverse():
        if not any(spec.satisfies(dep) for dep in dependencies):
            continue

        json_path = os.path.join(output_directory, f"{spec.name}.json")

        with open(json_path, "w") as fd:
            fd.write(spec.to_json(hash=ht.dag_hash))


def get_host_environment_metadata() -> Dict[str, str]:
    """Get the host environment, reduce to a subset that we can store in
    the install directory, and add the spack version.
    """
    import spack.main

    environ = get_host_environment()
    return {
        "host_os": environ["os"],
        "platform": environ["platform"],
        "host_target": environ["target"],
        "hostname": environ["hostname"],
        "spack_version": spack.main.get_version(),
        "kernel_version": platform.version(),
    }


def get_host_environment() -> Dict[str, Any]:
    """Return a dictionary (lookup) with host information (not including the
    os.environ).
    """
    host_platform = spack.platforms.host()
    host_target = host_platform.target("default_target")
    host_os = host_platform.operating_system("default_os")
    arch_fmt = "platform={0} os={1} target={2}"
    arch_spec = Spec(arch_fmt.format(host_platform, host_os, host_target))
    return {
        "target": str(host_target),
        "os": str(host_os),
        "platform": str(host_platform),
        "arch": arch_spec,
        "architecture": arch_spec,
        "arch_str": str(arch_spec),
        "hostname": socket.gethostname(),
    }


class SpecParseError(spack.error.SpecError):
    """Wrapper for ParseError for when we're parsing specs."""

    def __init__(self, parse_error):
        super().__init__(parse_error.message)
        self.string = parse_error.string
        self.pos = parse_error.pos

    @property
    def long_message(self):
        return "\n".join(
            [
                "  Encountered when parsing spec:",
                "    %s" % self.string,
                "    %s^" % (" " * self.pos),
            ]
        )


class ArchitecturePropagationError(spack.error.SpecError):
    """Raised when the double equal symbols are used to assign
    the spec's architecture.
    """


class DuplicateDependencyError(spack.error.SpecError):
    """Raised when the same dependency occurs in a spec twice."""


class MultipleVersionError(spack.error.SpecError):
    """Raised when version constraints occur in a spec twice."""


class DuplicateCompilerSpecError(spack.error.SpecError):
    """Raised when the same compiler occurs in a spec twice."""


class UnsupportedCompilerError(spack.error.SpecError):
    """Raised when the user asks for a compiler spack doesn't know about."""

    def __init__(self, compiler_name):
        super().__init__("The '%s' compiler is not yet supported." % compiler_name)


class DuplicateArchitectureError(spack.error.SpecError):
    """Raised when the same architecture occurs in a spec twice."""


class InconsistentSpecError(spack.error.SpecError):
    """Raised when two nodes in the same spec DAG have inconsistent
    constraints."""


class InvalidDependencyError(spack.error.SpecError):
    """Raised when a dependency in a spec is not actually a dependency
    of the package."""

    def __init__(self, pkg, deps):
        self.invalid_deps = deps
        super().__init__(
            "Package {0} does not depend on {1}".format(pkg, llnl.string.comma_or(deps))
        )


class NoProviderError(spack.error.SpecError):
    """Raised when there is no package that provides a particular
    virtual dependency.
    """

    def __init__(self, vpkg):
        super().__init__("No providers found for virtual package: '%s'" % vpkg)
        self.vpkg = vpkg


class MultipleProviderError(spack.error.SpecError):
    """Raised when there is no package that provides a particular
    virtual dependency.
    """

    def __init__(self, vpkg, providers):
        """Takes the name of the vpkg"""
        super().__init__(
            "Multiple providers found for '%s': %s" % (vpkg, [str(s) for s in providers])
        )
        self.vpkg = vpkg
        self.providers = providers


class UnsatisfiableSpecNameError(spack.error.UnsatisfiableSpecError):
    """Raised when two specs aren't even for the same package."""

    def __init__(self, provided, required):
        super().__init__(provided, required, "name")


class UnsatisfiableVersionSpecError(spack.error.UnsatisfiableSpecError):
    """Raised when a spec version conflicts with package constraints."""

    def __init__(self, provided, required):
        super().__init__(provided, required, "version")


class UnsatisfiableCompilerSpecError(spack.error.UnsatisfiableSpecError):
    """Raised when a spec comiler conflicts with package constraints."""

    def __init__(self, provided, required):
        super().__init__(provided, required, "compiler")


class UnsatisfiableCompilerFlagSpecError(spack.error.UnsatisfiableSpecError):
    """Raised when a spec variant conflicts with package constraints."""

    def __init__(self, provided, required):
        super().__init__(provided, required, "compiler_flags")


class UnsatisfiableArchitectureSpecError(spack.error.UnsatisfiableSpecError):
    """Raised when a spec architecture conflicts with package constraints."""

    def __init__(self, provided, required):
        super().__init__(provided, required, "architecture")


class UnsatisfiableProviderSpecError(spack.error.UnsatisfiableSpecError):
    """Raised when a provider is supplied but constraints don't match
    a vpkg requirement"""

    def __init__(self, provided, required):
        super().__init__(provided, required, "provider")


# TODO: get rid of this and be more specific about particular incompatible
# dep constraints
class UnsatisfiableDependencySpecError(spack.error.UnsatisfiableSpecError):
    """Raised when some dependency of constrained specs are incompatible"""

    def __init__(self, provided, required):
        super().__init__(provided, required, "dependency")


class UnconstrainableDependencySpecError(spack.error.SpecError):
    """Raised when attempting to constrain by an anonymous dependency spec"""

    def __init__(self, spec):
        msg = "Cannot constrain by spec '%s'. Cannot constrain by a" % spec
        msg += " spec containing anonymous dependencies"
        super().__init__(msg)


class AmbiguousHashError(spack.error.SpecError):
    def __init__(self, msg, *specs):
        spec_fmt = "{namespace}.{name}{@version}{%compiler}{compiler_flags}"
        spec_fmt += "{variants}{arch=architecture}{/hash:7}"
        specs_str = "\n  " + "\n  ".join(spec.format(spec_fmt) for spec in specs)
        super().__init__(msg + specs_str)


class InvalidHashError(spack.error.SpecError):
    def __init__(self, spec, hash):
        msg = f"No spec with hash {hash} could be found to match {spec}."
        msg += " Either the hash does not exist, or it does not match other spec constraints."
        super().__init__(msg)


class SpecFilenameError(spack.error.SpecError):
    """Raised when a spec file name is invalid."""


class NoSuchSpecFileError(SpecFilenameError):
    """Raised when a spec file doesn't exist."""


class SpecFormatStringError(spack.error.SpecError):
    """Called for errors in Spec format strings."""


class SpecFormatPathError(spack.error.SpecError):
    """Called for errors in Spec path-format strings."""


class SpecFormatSigilError(SpecFormatStringError):
    """Called for mismatched sigils and attributes in format strings"""

    def __init__(self, sigil, requirement, used):
        msg = "The sigil %s may only be used for %s." % (sigil, requirement)
        msg += " It was used with the attribute %s." % used
        super().__init__(msg)


class ConflictsInSpecError(spack.error.SpecError, RuntimeError):
    def __init__(self, spec, matches):
        message = 'Conflicts in concretized spec "{0}"\n'.format(spec.short_spec)

        visited = set()

        long_message = ""

        match_fmt_default = '{0}. "{1}" conflicts with "{2}"\n'
        match_fmt_custom = '{0}. "{1}" conflicts with "{2}" [{3}]\n'

        for idx, (s, c, w, msg) in enumerate(matches):
            if s not in visited:
                visited.add(s)
                long_message += "List of matching conflicts for spec:\n\n"
                long_message += s.tree(indent=4) + "\n"

            if msg is None:
                long_message += match_fmt_default.format(idx + 1, c, w)
            else:
                long_message += match_fmt_custom.format(idx + 1, c, w, msg)

        super().__init__(message, long_message)


class SpecDeprecatedError(spack.error.SpecError):
    """Raised when a spec concretizes to a deprecated spec or dependency."""


class InvalidSpecDetected(spack.error.SpecError):
    """Raised when a detected spec doesn't pass validation checks."""


class SpliceError(spack.error.SpecError):
    """Raised when a splice is not possible due to dependency or provider
    satisfaction mismatch. The resulting splice would be unusable."""
