# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

4. The name of the compiler to build with.

5. The versions of the compiler to build with.  Note that the identifier
   for a compiler version is the same '@' that is used for a package version.
   A version list denoted by '@' is associated with the compiler only if
   if it comes immediately after the compiler name.  Otherwise it will be
   associated with the current package spec.

6. The architecture to build with.  This is needed on machines where
   cross-compilation is required

Here is the EBNF grammar for a spec::

  spec-list    = { spec [ dep-list ] }
  dep_list     = { ^ spec }
  spec         = id [ options ]
  options      = { @version-list | +variant | -variant | ~variant |
                   %compiler | arch=architecture | [ flag ]=value}
  flag         = { cflags | cxxflags | fcflags | fflags | cppflags |
                   ldflags | ldlibs }
  variant      = id
  architecture = id
  compiler     = id [ version-list ]
  version-list = version [ { , version } ]
  version      = id | id: | :id | id:id
  id           = [A-Za-z0-9_][A-Za-z0-9_.-]*

Identifiers using the <name>=<value> command, such as architectures and
compiler flags, require a space before the name.

There is one context-sensitive part: ids in versions may contain '.', while
other ids may not.

There is one ambiguity: since '-' is allowed in an id, you need to put
whitespace space before -variant for it to be tokenized properly.  You can
either use whitespace, or you can just use ~variant since it means the same
thing.  Spack uses ~variant in directory names and in the canonical form of
specs to avoid ambiguity.  Both are provided because ~ can cause shell
expansion when it is the first character in an id typed on the command line.
"""
import base64
import sys
import collections
import hashlib
import itertools
import operator
import os
import re

import six
import ruamel.yaml as yaml

import llnl.util.filesystem as fs
import llnl.util.lang as lang
import llnl.util.tty.color as clr
import llnl.util.tty as tty

import spack.paths
import spack.architecture
import spack.compiler
import spack.compilers as compilers
import spack.config
import spack.dependency as dp
import spack.error
import spack.hash_types as ht
import spack.parse
import spack.provider_index
import spack.repo
import spack.solver
import spack.store
import spack.util.crypto
import spack.util.executable
import spack.util.module_cmd as md
import spack.util.prefix
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.util.string
import spack.variant as vt
import spack.version as vn


if sys.version_info >= (3, 3):
    from collections.abc import Mapping  # novm
else:
    from collections import Mapping


__all__ = [
    'Spec',
    'parse',
    'SpecParseError',
    'DuplicateDependencyError',
    'DuplicateCompilerSpecError',
    'UnsupportedCompilerError',
    'DuplicateArchitectureError',
    'InconsistentSpecError',
    'InvalidDependencyError',
    'NoProviderError',
    'MultipleProviderError',
    'UnsatisfiableSpecNameError',
    'UnsatisfiableVersionSpecError',
    'UnsatisfiableCompilerSpecError',
    'UnsatisfiableCompilerFlagSpecError',
    'UnsatisfiableArchitectureSpecError',
    'UnsatisfiableProviderSpecError',
    'UnsatisfiableDependencySpecError',
    'AmbiguousHashError',
    'InvalidHashError',
    'NoSuchHashError',
    'RedundantSpecError']

#: Valid pattern for an identifier in Spack
identifier_re = r'\w[\w-]*'

compiler_color = '@g'          #: color for highlighting compilers
version_color = '@c'           #: color for highlighting versions
architecture_color = '@m'      #: color for highlighting architectures
enabled_variant_color = '@B'   #: color for highlighting enabled variants
disabled_variant_color = '@r'  #: color for highlighting disabled varaints
dependency_color = '@.'        #: color for highlighting dependencies
hash_color = '@K'              #: color for highlighting package hashes

#: This map determines the coloring of specs when using color output.
#: We make the fields different colors to enhance readability.
#: See llnl.util.tty.color for descriptions of the color codes.
color_formats = {'%': compiler_color,
                 '@': version_color,
                 '=': architecture_color,
                 '+': enabled_variant_color,
                 '~': disabled_variant_color,
                 '^': dependency_color,
                 '#': hash_color}

#: Regex used for splitting by spec field separators.
#: These need to be escaped to avoid metacharacters in
#: ``color_formats.keys()``.
_separators = '[\\%s]' % '\\'.join(color_formats.keys())

#: Versionlist constant so we don't have to build a list
#: every time we call str()
_any_version = vn.VersionList([':'])

default_format = '{name}{@version}'
default_format += '{%compiler.name}{@compiler.version}{compiler_flags}'
default_format += '{variants}{arch=architecture}'


def colorize_spec(spec):
    """Returns a spec colorized according to the colors specified in
       color_formats."""
    class insert_color:

        def __init__(self):
            self.last = None

        def __call__(self, match):
            # ignore compiler versions (color same as compiler)
            sep = match.group(0)
            if self.last == '%' and sep == '@':
                return clr.cescape(sep)
            self.last = sep

            return '%s%s' % (color_formats[sep], clr.cescape(sep))

    return clr.colorize(re.sub(_separators, insert_color(), str(spec)) + '@.')


@lang.key_ordering
class ArchSpec(object):
    def __init__(self, spec_or_platform_tuple=(None, None, None)):
        """ Architecture specification a package should be built with.

        Each ArchSpec is comprised of three elements: a platform (e.g. Linux),
        an OS (e.g. RHEL6), and a target (e.g. x86_64).

        Args:
            spec_or_platform_tuple (ArchSpec or str or tuple): if an ArchSpec
                is passed it will be duplicated into the new instance.
                Otherwise information on platform, OS and target should be
                passed in either as a spec string or as a tuple.
        """
        # If another instance of ArchSpec was passed, duplicate it
        if isinstance(spec_or_platform_tuple, ArchSpec):
            self._dup(spec_or_platform_tuple)
            return

        # If the argument to __init__ is a spec string, parse it
        # and construct an ArchSpec
        def _string_or_none(s):
            if s and s != 'None':
                return str(s)
            return None

        if isinstance(spec_or_platform_tuple, six.string_types):
            spec_fields = spec_or_platform_tuple.split("-")
            msg = "invalid arch spec [{0}]"
            assert len(spec_fields) == 3, msg.format(spec_or_platform_tuple)

            platform, operating_system, target = spec_fields
            platform_tuple = _string_or_none(platform),\
                _string_or_none(operating_system), target

        if isinstance(spec_or_platform_tuple, tuple):
            platform, operating_system, target = spec_or_platform_tuple
            platform_tuple = _string_or_none(platform), \
                _string_or_none(operating_system), target
            msg = "invalid arch spec tuple [{0}]"
            assert len(platform_tuple) == 3, msg.format(platform_tuple)

        self.platform, self.os, self.target = platform_tuple

    def _autospec(self, spec_like):
        if isinstance(spec_like, ArchSpec):
            return spec_like
        return ArchSpec(spec_like)

    def _cmp_key(self):
        return self.platform, self.os, self.target

    def _dup(self, other):
        self.platform = other.platform
        self.os = other.os
        self.target = other.target

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

        if value in spack.architecture.Platform.reserved_oss:
            curr_platform = str(spack.architecture.platform())
            self.platform = self.platform or curr_platform

            if self.platform != curr_platform:
                raise ValueError(
                    "Can't set arch spec OS to reserved value '%s' when the "
                    "arch platform (%s) isn't the current platform (%s)" %
                    (value, self.platform, curr_platform))

            spec_platform = spack.architecture.get_platform(self.platform)
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
            if isinstance(t, spack.architecture.Target):
                return t
            if t and t != 'None':
                return spack.architecture.Target(t)
            return None

        value = target_or_none(value)

        if str(value) in spack.architecture.Platform.reserved_targets:
            curr_platform = str(spack.architecture.platform())
            self.platform = self.platform or curr_platform

            if self.platform != curr_platform:
                raise ValueError(
                    "Can't set arch spec target to reserved value '%s' when "
                    "the arch platform (%s) isn't the current platform (%s)" %
                    (value, self.platform, curr_platform))

            spec_platform = spack.architecture.get_platform(self.platform)
            value = spec_platform.target(value)

        self._target = value

    def satisfies(self, other, strict=False):
        """Predicate to check if this spec satisfies a constraint.

        Args:
            other (ArchSpec or str): constraint on the current instance
            strict (bool): if ``False`` the function checks if the current
                instance *might* eventually satisfy the constraint. If
                ``True`` it check if the constraint is satisfied right now.

        Returns:
            True if the constraint is satisfied, False otherwise.
        """
        other = self._autospec(other)

        # Check platform and os
        for attribute in ('platform', 'os'):
            other_attribute = getattr(other, attribute)
            self_attribute = getattr(self, attribute)
            if strict or self.concrete:
                if other_attribute and self_attribute != other_attribute:
                    return False
            else:
                if other_attribute and self_attribute and \
                        self_attribute != other_attribute:
                    return False

        # Check target
        return self.target_satisfies(other, strict=strict)

    def target_satisfies(self, other, strict):
        need_to_check = bool(other.target) if strict or self.concrete \
            else bool(other.target and self.target)

        # If there's no need to check we are fine
        if not need_to_check:
            return True

        # self is not concrete, but other_target is there and strict=True
        if self.target is None:
            return False

        return bool(self.target_intersection(other))

    def target_constrain(self, other):
        if not other.target_satisfies(self, strict=False):
            raise UnsatisfiableArchitectureSpecError(self, other)

        if self.target_concrete:
            return False
        elif other.target_concrete:
            self.target = other.target
            return True

        # Compute the intersection of every combination of ranges in the lists
        results = self.target_intersection(other)
        # Do we need to dedupe here?
        self.target = ','.join(results)

    def target_intersection(self, other):
        results = []

        if not self.target or not other.target:
            return results

        for s_target_range in str(self.target).split(','):
            s_min, s_sep, s_max = s_target_range.partition(':')
            for o_target_range in str(other.target).split(','):
                o_min, o_sep, o_max = o_target_range.partition(':')

                if not s_sep:
                    # s_target_range is a concrete target
                    # get a microarchitecture reference for at least one side
                    # of each comparison so we can use archspec comparators
                    s_comp = spack.architecture.Target(s_min).microarchitecture
                    if not o_sep:
                        if s_min == o_min:
                            results.append(s_min)
                    elif (not o_min or s_comp >= o_min) and (
                            not o_max or s_comp <= o_max):
                        results.append(s_min)
                elif not o_sep:
                    # "cast" to microarchitecture
                    o_comp = spack.architecture.Target(o_min).microarchitecture
                    if (not s_min or o_comp >= s_min) and (
                            not s_max or o_comp <= s_max):
                        results.append(o_min)
                else:
                    # Take intersection of two ranges
                    # Lots of comparisons needed
                    _s_min = spack.architecture.Target(s_min).microarchitecture
                    _s_max = spack.architecture.Target(s_max).microarchitecture
                    _o_min = spack.architecture.Target(o_min).microarchitecture
                    _o_max = spack.architecture.Target(o_max).microarchitecture

                    n_min = s_min if _s_min >= _o_min else o_min
                    n_max = s_max if _s_max <= _o_max else o_max
                    _n_min = spack.architecture.Target(n_min).microarchitecture
                    _n_max = spack.architecture.Target(n_max).microarchitecture
                    if _n_min == _n_max:
                        results.append(n_min)
                    elif not n_min or not n_max or _n_min < _n_max:
                        results.append('%s:%s' % (n_min, n_max))
        return results

    def constrain(self, other):
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

        if not other.satisfies(self):
            raise UnsatisfiableArchitectureSpecError(other, self)

        constrained = False
        for attr in ('platform', 'os'):
            svalue, ovalue = getattr(self, attr), getattr(other, attr)
            if svalue is None and ovalue is not None:
                setattr(self, attr, ovalue)
                constrained = True

        self.target_constrain(other)

        return constrained

    def copy(self):
        """Copy the current instance and returns the clone."""
        clone = ArchSpec.__new__(ArchSpec)
        clone._dup(self)
        return clone

    @property
    def concrete(self):
        """True if the spec is concrete, False otherwise"""
        # return all(v for k, v in six.iteritems(self.to_cmp_dict()))
        return (self.platform and self.os and self.target and
                self.target_concrete)

    @property
    def target_concrete(self):
        """True if the target is not a range or list."""
        return ':' not in str(self.target) and ',' not in str(self.target)

    def to_dict(self):
        d = syaml.syaml_dict([
            ('platform', self.platform),
            ('platform_os', self.os),
            ('target', self.target.to_dict_or_value())])
        return syaml.syaml_dict([('arch', d)])

    @staticmethod
    def from_dict(d):
        """Import an ArchSpec from raw YAML/JSON data.

        This routine implements a measure of compatibility with older
        versions of Spack.  Spack releases before 0.10 used a single
        string with no OS or platform identifiers.  We import old Spack
        architectures with platform ``spack09``, OS ``unknown``, and the
        old arch string as the target.

        Specs from `0.10` or later have a more fleshed out architecture
        descriptor with a platform, an OS, and a target.

        """
        if not isinstance(d['arch'], dict):
            return ArchSpec(('spack09', 'unknown', d['arch']))

        d = d['arch']

        operating_system = d.get('platform_os', None) or d['os']
        target = spack.architecture.Target.from_dict_or_value(d['target'])

        return ArchSpec((d['platform'], operating_system, target))

    def __str__(self):
        return "%s-%s-%s" % (self.platform, self.os, self.target)

    def __repr__(self):
        # TODO: this needs to be changed (repr is meant to return valid
        # TODO: Python code to return an instance equivalent to the current
        # TODO: one).
        return str(self)

    def __contains__(self, string):
        return string in str(self) or string in self.target


@lang.key_ordering
class CompilerSpec(object):
    """The CompilerSpec field represents the compiler or range of compiler
       versions that a package should be built with.  CompilerSpecs have a
       name and a version list. """

    def __init__(self, *args):
        nargs = len(args)
        if nargs == 1:
            arg = args[0]
            # If there is one argument, it's either another CompilerSpec
            # to copy or a string to parse
            if isinstance(arg, six.string_types):
                c = SpecParser().parse_compiler(arg)
                self.name = c.name
                self.versions = c.versions

            elif isinstance(arg, CompilerSpec):
                self.name = arg.name
                self.versions = arg.versions.copy()

            else:
                raise TypeError(
                    "Can only build CompilerSpec from string or " +
                    "CompilerSpec. Found %s" % type(arg))

        elif nargs == 2:
            name, version = args
            self.name = name
            self.versions = vn.VersionList()
            self.versions.add(vn.ver(version))

        else:
            raise TypeError(
                "__init__ takes 1 or 2 arguments. (%d given)" % nargs)

    def _add_versions(self, version_list):
        # If it already has a non-trivial version list, this is an error
        if self.versions and self.versions != vn.VersionList(':'):
            # Note: This may be impossible to reach by the current parser
            # Keeping it in case the implementation changes.
            raise MultipleVersionError(
                'A spec cannot contain multiple version signifiers.'
                ' Use a version list instead.')
        self.versions = vn.VersionList()
        for version in version_list:
            self.versions.add(version)

    def _autospec(self, compiler_spec_like):
        if isinstance(compiler_spec_like, CompilerSpec):
            return compiler_spec_like
        return CompilerSpec(compiler_spec_like)

    def satisfies(self, other, strict=False):
        other = self._autospec(other)
        return (self.name == other.name and
                self.versions.satisfies(other.versions, strict=strict))

    def constrain(self, other):
        """Intersect self's versions with other.

        Return whether the CompilerSpec changed.
        """
        other = self._autospec(other)

        # ensure that other will actually constrain this spec.
        if not other.satisfies(self):
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

    def _cmp_key(self):
        return (self.name, self.versions)

    def to_dict(self):
        d = syaml.syaml_dict([('name', self.name)])
        d.update(self.versions.to_dict())

        return syaml.syaml_dict([('compiler', d)])

    @staticmethod
    def from_dict(d):
        d = d['compiler']
        return CompilerSpec(d['name'], vn.VersionList.from_dict(d))

    def __str__(self):
        out = self.name
        if self.versions and self.versions != _any_version:
            vlist = ",".join(str(v) for v in self.versions)
            out += "@%s" % vlist
        return out

    def __repr__(self):
        return str(self)


@lang.key_ordering
class DependencySpec(object):
    """DependencySpecs connect two nodes in the DAG, and contain deptypes.

    Dependencies can be one (or more) of several types:

    - build: needs to be in the PATH at build time.
    - link: is linked to and added to compiler flags.
    - run: needs to be in the PATH for the package to run.

    Fields:
    - spec: Spec depended on by parent.
    - parent: Spec that depends on `spec`.
    - deptypes: list of strings, representing dependency relationships.
    """

    def __init__(self, parent, spec, deptypes):
        self.parent = parent
        self.spec = spec
        self.deptypes = tuple(sorted(set(deptypes)))

    def update_deptypes(self, deptypes):
        deptypes = set(deptypes)
        deptypes.update(self.deptypes)
        deptypes = tuple(sorted(deptypes))
        changed = self.deptypes != deptypes

        self.deptypes = deptypes
        return changed

    def copy(self):
        return DependencySpec(self.parent, self.spec, self.deptypes)

    def add_type(self, type):
        self.deptypes = dp.canonical_deptype(
            self.deptypes + dp.canonical_deptype(type)
        )

    def _cmp_key(self):
        return (self.parent.name if self.parent else None,
                self.spec.name if self.spec else None,
                self.deptypes)

    def __str__(self):
        return "%s %s--> %s" % (self.parent.name if self.parent else None,
                                self.deptypes,
                                self.spec.name if self.spec else None)


_valid_compiler_flags = [
    'cflags', 'cxxflags', 'fflags', 'ldflags', 'ldlibs', 'cppflags']


class FlagMap(lang.HashableMap):

    def __init__(self, spec):
        super(FlagMap, self).__init__()
        self.spec = spec

    def satisfies(self, other, strict=False):
        if strict or (self.spec and self.spec._concrete):
            return all(f in self and set(self[f]) == set(other[f])
                       for f in other)
        else:
            return all(set(self[f]) == set(other[f])
                       for f in other if (other[f] != [] and f in self))

    def constrain(self, other):
        """Add all flags in other that aren't in self to self.

        Return whether the spec changed.
        """
        if other.spec and other.spec._concrete:
            for k in self:
                if k not in other:
                    raise UnsatisfiableCompilerFlagSpecError(
                        self[k], '<absent>')

        changed = False
        for k in other:
            if k in self and not set(self[k]) <= set(other[k]):
                raise UnsatisfiableCompilerFlagSpecError(
                    ' '.join(f for f in self[k]),
                    ' '.join(f for f in other[k]))
            elif k not in self:
                self[k] = other[k]
                changed = True
        return changed

    @staticmethod
    def valid_compiler_flags():
        return _valid_compiler_flags

    def copy(self):
        clone = FlagMap(None)
        for name, value in self.items():
            clone[name] = value
        return clone

    def _cmp_key(self):
        return tuple((k, tuple(v)) for k, v in sorted(six.iteritems(self)))

    def __str__(self):
        sorted_keys = [k for k in sorted(self.keys()) if self[k] != []]
        cond_symbol = ' ' if len(sorted_keys) > 0 else ''
        return cond_symbol + ' '.join(
            str(key) + '=\"' + ' '.join(
                str(f) for f in self[key]) + '\"'
            for key in sorted_keys) + cond_symbol


class DependencyMap(lang.HashableMap):
    """Each spec has a DependencyMap containing specs for its dependencies.
       The DependencyMap is keyed by name. """

    def __str__(self):
        return "{deps: %s}" % ', '.join(str(d) for d in sorted(self.values()))


def _command_default_handler(descriptor, spec, cls):
    """Default handler when looking for the 'command' attribute.

    Tries to search for ``spec.name`` in the ``spec.prefix.bin`` directory.

    Parameters:
        descriptor (ForwardQueryToPackage): descriptor that triggered the call
        spec (Spec): spec that is being queried
        cls (type(spec)): type of spec, to match the signature of the
            descriptor ``__get__`` method

    Returns:
        Executable: An executable of the command

    Raises:
        RuntimeError: If the command is not found
    """
    path = os.path.join(spec.prefix.bin, spec.name)

    if fs.is_exe(path):
        return spack.util.executable.Executable(path)
    else:
        msg = 'Unable to locate {0} command in {1}'
        raise RuntimeError(msg.format(spec.name, spec.prefix.bin))


def _headers_default_handler(descriptor, spec, cls):
    """Default handler when looking for the 'headers' attribute.

    Tries to search for ``*.h`` files recursively starting from
    ``spec.prefix.include``.

    Parameters:
        descriptor (ForwardQueryToPackage): descriptor that triggered the call
        spec (Spec): spec that is being queried
        cls (type(spec)): type of spec, to match the signature of the
            descriptor ``__get__`` method

    Returns:
        HeaderList: The headers in ``prefix.include``

    Raises:
        NoHeadersError: If no headers are found
    """
    headers = fs.find_headers('*', root=spec.prefix.include, recursive=True)

    if headers:
        return headers
    else:
        msg = 'Unable to locate {0} headers in {1}'
        raise spack.error.NoHeadersError(
            msg.format(spec.name, spec.prefix.include))


def _libs_default_handler(descriptor, spec, cls):
    """Default handler when looking for the 'libs' attribute.

    Tries to search for ``lib{spec.name}`` recursively starting from
    ``spec.prefix``. If ``spec.name`` starts with ``lib``, searches for
    ``{spec.name}`` instead.

    Parameters:
        descriptor (ForwardQueryToPackage): descriptor that triggered the call
        spec (Spec): spec that is being queried
        cls (type(spec)): type of spec, to match the signature of the
            descriptor ``__get__`` method

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
    name = spec.name.replace('-', '?')

    # Avoid double 'lib' for packages whose names already start with lib
    if not name.startswith('lib'):
        name = 'lib' + name

    # If '+shared' search only for shared library; if '~shared' search only for
    # static library; otherwise, first search for shared and then for static.
    search_shared = [True] if ('+shared' in spec) else \
        ([False] if ('~shared' in spec) else [True, False])

    for shared in search_shared:
        libs = fs.find_libraries(
            name, spec.prefix, shared=shared, recursive=True)
        if libs:
            return libs

    msg = 'Unable to recursively locate {0} libraries in {1}'
    raise spack.error.NoLibrariesError(msg.format(spec.name, spec.prefix))


class ForwardQueryToPackage(object):
    """Descriptor used to forward queries from Spec to Package"""

    def __init__(self, attribute_name, default_handler=None):
        """Create a new descriptor.

        Parameters:
            attribute_name (str): name of the attribute to be
                searched for in the Package instance
            default_handler (callable, optional): default function to be
                called if the attribute was not found in the Package
                instance
        """
        self.attribute_name = attribute_name
        self.default = default_handler

    def __get__(self, instance, cls):
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
        pkg = instance.package
        try:
            query = instance.last_query
        except AttributeError:
            # There has been no query yet: this means
            # a spec is trying to access its own attributes
            _ = instance[instance.name]  # NOQA: ignore=F841
            query = instance.last_query

        callbacks_chain = []
        # First in the chain : specialized attribute for virtual packages
        if query.isvirtual:
            specialized_name = '{0}_{1}'.format(
                query.name, self.attribute_name
            )
            callbacks_chain.append(lambda: getattr(pkg, specialized_name))
        # Try to get the generic method from Package
        callbacks_chain.append(lambda: getattr(pkg, self.attribute_name))
        # Final resort : default callback
        if self.default is not None:
            callbacks_chain.append(lambda: self.default(self, instance, cls))

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
                    msg  = "Query of package '{name}' for '{attrib}' failed\n"
                    msg += "\tprefix : {spec.prefix}\n"
                    msg += "\tspec : {spec}\n"
                    msg += "\tqueried as : {query.name}\n"
                    msg += "\textra parameters : {query.extra_parameters}"
                    message = msg.format(
                        name=pkg.name, attrib=self.attribute_name,
                        spec=instance, query=instance.last_query)
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
        fmt = '\'{name}\' package has no relevant attribute \'{query}\'\n'
        fmt += '\tspec : \'{spec}\'\n'
        fmt += '\tqueried as : \'{spec.last_query.name}\'\n'
        fmt += '\textra parameters : \'{spec.last_query.extra_parameters}\'\n'
        message = fmt.format(
            name=pkg.name,
            query=self.attribute_name,
            spec=instance
        )
        raise AttributeError(message)

    def __set__(self, instance, value):
        cls_name = type(instance).__name__
        msg = "'{0}' object attribute '{1}' is read-only"
        raise AttributeError(msg.format(cls_name, self.attribute_name))


# Represents a query state in a BuildInterface object
QueryState = collections.namedtuple(
    'QueryState', ['name', 'extra_parameters', 'isvirtual']
)


class SpecBuildInterface(lang.ObjectWrapper):
    command = ForwardQueryToPackage(
        'command',
        default_handler=_command_default_handler
    )

    headers = ForwardQueryToPackage(
        'headers',
        default_handler=_headers_default_handler
    )

    libs = ForwardQueryToPackage(
        'libs',
        default_handler=_libs_default_handler
    )

    def __init__(self, spec, name, query_parameters):
        super(SpecBuildInterface, self).__init__(spec)

        is_virtual = spack.repo.path.is_virtual(name)
        self.last_query = QueryState(
            name=name,
            extra_parameters=query_parameters,
            isvirtual=is_virtual
        )


@lang.key_ordering
class Spec(object):

    #: Cache for spec's prefix, computed lazily in the corresponding property
    _prefix = None

    def __init__(self, spec_like=None,
                 normal=False, concrete=False, external_path=None,
                 external_modules=None, full_hash=None):
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
        self._full_hash = full_hash

        """

        # Copy if spec_like is a Spec.
        if isinstance(spec_like, Spec):
            self._dup(spec_like)
            return

        # init an empty spec that matches anything.
        self.name = None
        self.versions = vn.VersionList(':')
        self.variants = vt.VariantMap(self)
        self.architecture = None
        self.compiler = None
        self.compiler_flags = FlagMap(self)
        self._dependents = DependencyMap()
        self._dependencies = DependencyMap()
        self.namespace = None

        self._hash = None
        self._build_hash = None
        self._cmp_key_cache = None
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
        self.external_path = external_path
        self.external_modules = Spec._format_module_list(external_modules)
        self._full_hash = full_hash

        # Older spack versions did not compute full_hash or build_hash,
        # and we may not have the necessary information to recompute them
        # if we read in old specs. Old concrete specs are marked "final"
        # when read in to indicate that we shouldn't recompute full_hash
        # or build_hash. New specs are not final; we can lazily compute
        # their hashes.
        self._hashes_final = False

        # This attribute is used to store custom information for
        # external specs. None signal that it was not set yet.
        self.extra_attributes = None

        # This attribute holds the original build copy of the spec if it is
        # deployed differently than it was built. None signals that the spec
        # is deployed "as built."
        # Build spec should be the actual build spec unless marked dirty.
        self._build_spec = None

        if isinstance(spec_like, six.string_types):
            spec_list = SpecParser(self).parse(spec_like)
            if len(spec_list) > 1:
                raise ValueError("More than one spec in string: " + spec_like)
            if len(spec_list) < 1:
                raise ValueError("String contains no specs: " + spec_like)

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
    def external(self):
        return bool(self.external_path) or bool(self.external_modules)

    def get_dependency(self, name):
        dep = self._dependencies.get(name)
        if dep is not None:
            return dep
        raise InvalidDependencyError(self.name, name)

    def _find_deps(self, where, deptype):
        deptype = dp.canonical_deptype(deptype)

        return [dep for dep in where.values()
                if deptype and (not dep.deptypes or
                                any(d in deptype for d in dep.deptypes))]

    def dependencies(self, deptype='all'):
        return [d.spec
                for d in self._find_deps(self._dependencies, deptype)]

    def dependents(self, deptype='all'):
        return [d.parent
                for d in self._find_deps(self._dependents, deptype)]

    def dependencies_dict(self, deptype='all'):
        return dict((d.spec.name, d)
                    for d in self._find_deps(self._dependencies, deptype))

    def dependents_dict(self, deptype='all'):
        return dict((d.parent.name, d)
                    for d in self._find_deps(self._dependents, deptype))

    #
    # Private routines here are called by the parser when building a spec.
    #
    def _add_versions(self, version_list):
        """Called by the parser to add an allowable version."""
        # If it already has a non-trivial version list, this is an error
        if self.versions and self.versions != vn.VersionList(':'):
            raise MultipleVersionError(
                'A spec cannot contain multiple version signifiers.'
                ' Use a version list instead.')
        self.versions = vn.VersionList()
        for version in version_list:
            self.versions.add(version)

    def _add_flag(self, name, value):
        """Called by the parser to add a known flag.
        Known flags currently include "arch"
        """
        valid_flags = FlagMap.valid_compiler_flags()
        if name == 'arch' or name == 'architecture':
            parts = tuple(value.split('-'))
            plat, os, tgt = parts if len(parts) == 3 else (None, None, value)
            self._set_architecture(platform=plat, os=os, target=tgt)
        elif name == 'platform':
            self._set_architecture(platform=value)
        elif name == 'os' or name == 'operating_system':
            self._set_architecture(os=value)
        elif name == 'target':
            self._set_architecture(target=value)
        elif name in valid_flags:
            assert(self.compiler_flags is not None)
            self.compiler_flags[name] = spack.compiler.tokenize_flags(value)
        else:
            # FIXME:
            # All other flags represent variants. 'foo=true' and 'foo=false'
            # map to '+foo' and '~foo' respectively. As such they need a
            # BoolValuedVariant instance.
            if str(value).upper() == 'TRUE' or str(value).upper() == 'FALSE':
                self.variants[name] = vt.BoolValuedVariant(name, value)
            else:
                self.variants[name] = vt.AbstractVariant(name, value)

    def _set_architecture(self, **kwargs):
        """Called by the parser to set the architecture."""
        arch_attrs = ['platform', 'os', 'target']
        if self.architecture and self.architecture.concrete:
            raise DuplicateArchitectureError(
                "Spec for '%s' cannot have two architectures." % self.name)

        if not self.architecture:
            new_vals = tuple(kwargs.get(arg, None) for arg in arch_attrs)
            self.architecture = ArchSpec(new_vals)
        else:
            new_attrvals = [(a, v) for a, v in six.iteritems(kwargs)
                            if a in arch_attrs]
            for new_attr, new_value in new_attrvals:
                if getattr(self.architecture, new_attr):
                    raise DuplicateArchitectureError(
                        "Spec for '%s' cannot have two '%s' specified "
                        "for its architecture" % (self.name, new_attr))
                else:
                    setattr(self.architecture, new_attr, new_value)

    def _set_compiler(self, compiler):
        """Called by the parser to set the compiler."""
        if self.compiler:
            raise DuplicateCompilerSpecError(
                "Spec for '%s' cannot have two compilers." % self.name)
        self.compiler = compiler

    def _add_dependency(self, spec, deptypes):
        """Called by the parser to add another spec as a dependency."""
        if spec.name in self._dependencies:
            raise DuplicateDependencyError(
                "Cannot depend on '%s' twice" % spec)

        # create an edge and add to parent and child
        dspec = DependencySpec(self, spec, deptypes)
        self._dependencies[spec.name] = dspec
        spec._dependents[self.name] = dspec

    def _add_default_platform(self):
        """If a spec has an os or a target and no platform, give it
           the default platform.

           This is private because it is used by the parser -- it's not
           expected to be used outside of ``spec.py``.

        """
        arch = self.architecture
        if arch and not arch.platform and (arch.os or arch.target):
            self._set_architecture(platform=spack.architecture.platform().name)

    #
    # Public interface
    #
    @property
    def fullname(self):
        return (
            ('%s.%s' % (self.namespace, self.name)) if self.namespace else
            (self.name if self.name else ''))

    @property
    def root(self):
        """Follow dependent links and find the root of this spec's DAG.

        Spack specs have a single root (the package being installed).
        """
        if not self._dependents:
            return self

        return next(iter(self._dependents.values())).parent.root

    @property
    def package(self):
        if not self._package:
            self._package = spack.repo.get(self)
        return self._package

    @property
    def package_class(self):
        """Internal package call gets only the class object for a package.
           Use this to just get package metadata.
        """
        return spack.repo.path.get_pkg_class(self.fullname)

    @property
    def virtual(self):
        """Right now, a spec is virtual if no package exists with its name.

           TODO: revisit this -- might need to use a separate namespace and
           be more explicit about this.
           Possible idea: just use conventin and make virtual deps all
           caps, e.g., MPI vs mpi.
        """
        # This method can be called while regenerating the provider index
        # So we turn off using the index to detect virtuals
        return spack.repo.path.is_virtual(self.name, use_index=False)

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

    def traverse(self, **kwargs):
        direction = kwargs.get('direction', 'children')
        depth = kwargs.get('depth', False)

        get_spec = lambda s: s.spec
        if direction == 'parents':
            get_spec = lambda s: s.parent

        if depth:
            for d, dspec in self.traverse_edges(**kwargs):
                yield d, get_spec(dspec)
        else:
            for dspec in self.traverse_edges(**kwargs):
                yield get_spec(dspec)

    def traverse_edges(self, visited=None, d=0, deptype='all',
                       dep_spec=None, **kwargs):
        """Generic traversal of the DAG represented by this spec.
           This will yield each node in the spec.  Options:

           order    [=pre|post]
               Order to traverse spec nodes. Defaults to preorder traversal.
               Options are:

               'pre':  Pre-order traversal; each node is yielded before its
                       children in the dependency DAG.
               'post': Post-order  traversal; each node is yielded after its
                       children in the dependency DAG.

           cover    [=nodes|edges|paths]
               Determines how extensively to cover the dag.  Possible values:

               'nodes': Visit each node in the dag only once.  Every node
                        yielded by this function will be unique.
               'edges': If a node has been visited once but is reached along a
                        new path from the root, yield it but do not descend
                        into it.  This traverses each 'edge' in the DAG once.
               'paths': Explore every unique path reachable from the root.
                        This descends into visited subtrees and will yield
                        nodes twice if they're reachable by multiple paths.

           depth    [=False]
               Defaults to False.  When True, yields not just nodes in the
               spec, but also their depth from the root in a (depth, node)
               tuple.

           key   [=id]
               Allow a custom key function to track the identity of nodes
               in the traversal.

           root     [=True]
               If False, this won't yield the root node, just its descendents.

           direction [=children|parents]
               If 'children', does a traversal of this spec's children.  If
               'parents', traverses upwards in the DAG towards the root.

        """
        # get initial values for kwargs
        depth = kwargs.get('depth', False)
        key_fun = kwargs.get('key', id)
        if isinstance(key_fun, six.string_types):
            key_fun = operator.attrgetter(key_fun)
        yield_root = kwargs.get('root', True)
        cover = kwargs.get('cover', 'nodes')
        direction = kwargs.get('direction', 'children')
        order = kwargs.get('order', 'pre')
        deptype = dp.canonical_deptype(deptype)

        # Make sure kwargs have legal values; raise ValueError if not.
        def validate(name, val, allowed_values):
            if val not in allowed_values:
                raise ValueError("Invalid value for %s: %s.  Choices are %s"
                                 % (name, val, ",".join(allowed_values)))
        validate('cover',     cover,     ('nodes', 'edges', 'paths'))
        validate('direction', direction, ('children', 'parents'))
        validate('order',     order,     ('pre', 'post'))

        if visited is None:
            visited = set()
        key = key_fun(self)

        # Node traversal does not yield visited nodes.
        if key in visited and cover == 'nodes':
            return

        def return_val(dspec):
            if not dspec:
                # make a fake dspec for the root.
                if direction == 'parents':
                    dspec = DependencySpec(self, None, ())
                else:
                    dspec = DependencySpec(None, self, ())
            return (d, dspec) if depth else dspec

        yield_me = yield_root or d > 0

        # Preorder traversal yields before successors
        if yield_me and order == 'pre':
            yield return_val(dep_spec)

        # Edge traversal yields but skips children of visited nodes
        if not (key in visited and cover == 'edges'):
            visited.add(key)

            # This code determines direction and yields the children/parents
            if direction == 'children':
                where = self._dependencies
                succ = lambda dspec: dspec.spec
            elif direction == 'parents':
                where = self._dependents
                succ = lambda dspec: dspec.parent
            else:
                raise ValueError('Invalid traversal direction: %s' % direction)

            for name, dspec in sorted(where.items()):
                dt = dspec.deptypes
                if dt and not any(d in deptype for d in dt):
                    continue

                for child in succ(dspec).traverse_edges(
                        visited, d + 1, deptype, dspec, **kwargs):
                    yield child

        # Postorder traversal yields after successors
        if yield_me and order == 'post':
            yield return_val(dep_spec)

    @property
    def short_spec(self):
        """Returns a version of the spec with the dependencies hashed
           instead of completely enumerated."""
        spec_format = '{name}{@version}{%compiler}'
        spec_format += '{variants}{arch=architecture}{/hash:7}'
        return self.format(spec_format)

    @property
    def cshort_spec(self):
        """Returns an auto-colorized version of ``self.short_spec``."""
        spec_format = '{name}{@version}{%compiler}'
        spec_format += '{variants}{arch=architecture}{/hash:7}'
        return self.cformat(spec_format)

    @property
    def prefix(self):
        if not self._concrete:
            raise spack.error.SpecError("Spec is not concrete: " + str(self))

        if self._prefix is None:
            upstream, record = spack.store.db.query_by_spec_hash(
                self.dag_hash())
            if record and record.path:
                self.prefix = record.path
            else:
                self.prefix = spack.store.layout.path_for_spec(self)
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = spack.util.prefix.Prefix(value)

    def _spec_hash(self, hash):
        """Utility method for computing different types of Spec hashes.

        Arguments:
            hash (SpecHashDescriptor): type of hash to generate.
        """
        # TODO: curently we strip build dependencies by default.  Rethink
        # this when we move to using package hashing on all specs.
        node_dict = self.to_node_dict(hash=hash)
        yaml_text = syaml.dump(node_dict, default_flow_style=True)
        sha = hashlib.sha1(yaml_text.encode('utf-8'))
        b32_hash = base64.b32encode(sha.digest()).lower()

        if sys.version_info[0] >= 3:
            b32_hash = b32_hash.decode('utf-8')

        return b32_hash

    def _cached_hash(self, hash, length=None):
        """Helper function for storing a cached hash on the spec.

        This will run _spec_hash() with the deptype and package_hash
        parameters, and if this spec is concrete, it will store the value
        in the supplied attribute on this spec.

        Arguments:
            hash (SpecHashDescriptor): type of hash to generate.
        """
        if not hash.attr:
            return self._spec_hash(hash)[:length]

        hash_string = getattr(self, hash.attr, None)
        if hash_string:
            return hash_string[:length]
        else:
            hash_string = self._spec_hash(hash)
            if self.concrete:
                setattr(self, hash.attr, hash_string)

            return hash_string[:length]

    def dag_hash(self, length=None):
        """This is Spack's default hash, used to identify installations.

        At the moment, it excludes build dependencies to avoid rebuilding
        packages whenever build dependency versions change. We will
        revise this to include more detailed provenance when the
        concretizer can more aggressievly reuse installed dependencies.
        """
        return self._cached_hash(ht.dag_hash, length)

    def build_hash(self, length=None):
        """Hash used to store specs in environments.

        This hash includes build dependencies, and we need to preserve
        them to be able to rebuild an entire environment for a user.
        """
        return self._cached_hash(ht.build_hash, length)

    def full_hash(self, length=None):
        """Hash  to determine when to rebuild packages in the build pipeline.

        This hash includes the package hash, so that we know when package
        files has changed between builds. It does not currently include
        build dependencies, though it likely should.

        TODO: investigate whether to include build deps here.
        """
        return self._cached_hash(ht.full_hash, length)

    def dag_hash_bit_prefix(self, bits):
        """Get the first <bits> bits of the DAG hash as an integer type."""
        return base32_prefix_bits(self.dag_hash(), bits)

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
            hash (SpecHashDescriptor) type of hash to generate.
         """
        d = syaml.syaml_dict()

        if self.versions:
            d.update(self.versions.to_dict())

        if self.architecture:
            d.update(self.architecture.to_dict())

        if self.compiler:
            d.update(self.compiler.to_dict())

        if self.namespace:
            d['namespace'] = self.namespace

        params = syaml.syaml_dict(
            sorted(
                v.yaml_entry() for _, v in self.variants.items()
            )
        )

        params.update(sorted(self.compiler_flags.items()))
        if params:
            d['parameters'] = params

        if self.external:
            d['external'] = syaml.syaml_dict([
                ('path', self.external_path),
                ('module', self.external_modules),
                ('extra_attributes', self.extra_attributes)
            ])

        if not self._concrete:
            d['concrete'] = False

        if 'patches' in self.variants:
            variant = self.variants['patches']
            if hasattr(variant, '_patches_in_order_of_appearance'):
                d['patches'] = variant._patches_in_order_of_appearance

        if hash.package_hash:
            d['package_hash'] = self.package.content_hash()

        deps = self.dependencies_dict(deptype=hash.deptype)
        if deps:
            d['dependencies'] = syaml.syaml_dict([
                (name,
                 syaml.syaml_dict([
                     ('hash', dspec.spec._cached_hash(hash)),
                     ('type', sorted(str(s) for s in dspec.deptypes))])
                 ) for name, dspec in sorted(deps.items())
            ])

        return syaml.syaml_dict([(self.name, d)])

    def to_dict(self, hash=ht.dag_hash):
        """Create a dictionary suitable for writing this spec to YAML or JSON.

        This dictionaries like the one that is ultimately written to a
        ``spec.yaml`` file in each Spack installation directory.  For
        example, for sqlite::

            {
                'spec': [
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
                            'hash': '722dzmgymxyxd6ovjvh4742kcetkqtfs'
                        }
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
        node_list = []
        for s in self.traverse(order='pre', deptype=hash.deptype):
            node_list.append(s.node_dict_with_hashes(hash))

        return syaml.syaml_dict([('spec', node_list)])

    def node_dict_with_hashes(self, hash=ht.dag_hash):
        """ Returns a node_dict of this spec with the dag hash added.  If this
        spec is concrete, the full hash is added as well.  If 'build' is in
        the hash_type, the build hash is also added. """
        node = self.to_node_dict(hash)
        node[self.name]['hash'] = self.dag_hash()

        # full_hash and build_hash are lazily computed -- but if we write
        # a spec out, we want them to be included. This is effectively
        # the last chance we get to compute them accurately.
        if self.concrete:
            # build and full hashes can be written out if:
            # 1. they're precomputed (i.e. we read them from somewhere
            #    and they were already on the spec
            # 2. we can still compute them lazily (i.e. we just made them and
            #    have the full dependency graph on-hand)
            #
            # we want to avoid recomputing either hash for specs we read
            # in from the DB or elsewhere, as we may not have the info
            # (like patches, package versions, etc.) that we need to
            # compute them. Unknown hashes are better than wrong hashes.
            write_full_hash = (
                self._hashes_final and self._full_hash or   # cached and final
                not self._hashes_final)                     # lazily compute
            write_build_hash = 'build' in hash.deptype and (
                self._hashes_final and self._build_hash or  # cached and final
                not self._hashes_final)                     # lazily compute

            if write_full_hash:
                node[self.name]['full_hash'] = self.full_hash()
            if write_build_hash:
                node[self.name]['build_hash'] = self.build_hash()

        return node

    def to_record_dict(self):
        """Return a "flat" dictionary with name and hash as top-level keys.

        This is similar to ``to_node_dict()``, but the name and the hash
        are "flattened" into the dictionary for easiler parsing by tools
        like ``jq``.  Instead of being keyed by name or hash, the
        dictionary "name" and "hash" fields, e.g.::

            {
              "name": "openssl"
              "hash": "3ws7bsihwbn44ghf6ep4s6h4y2o6eznv"
              "version": "3.28.0",
              "arch": {
              ...
            }

        But is otherwise the same as ``to_node_dict()``.

        """
        dictionary = syaml.syaml_dict()
        dictionary["name"] = self.name
        dictionary["hash"] = self.dag_hash()
        dictionary.update(self.to_node_dict()[self.name])
        return dictionary

    def to_yaml(self, stream=None, hash=ht.dag_hash):
        return syaml.dump(
            self.to_dict(hash), stream=stream, default_flow_style=False)

    def to_json(self, stream=None, hash=ht.dag_hash):
        return sjson.dump(self.to_dict(hash), stream)

    @staticmethod
    def from_node_dict(node):
        name = next(iter(node))
        node = node[name]

        spec = Spec()
        spec.name = name
        spec.namespace = node.get('namespace', None)
        spec._hash = node.get('hash', None)
        spec._build_hash = node.get('build_hash', None)
        spec._full_hash = node.get('full_hash', None)

        if 'version' in node or 'versions' in node:
            spec.versions = vn.VersionList.from_dict(node)

        if 'arch' in node:
            spec.architecture = ArchSpec.from_dict(node)

        if 'compiler' in node:
            spec.compiler = CompilerSpec.from_dict(node)
        else:
            spec.compiler = None

        if 'parameters' in node:
            for name, value in node['parameters'].items():
                if name in _valid_compiler_flags:
                    spec.compiler_flags[name] = value
                else:
                    spec.variants[name] = vt.MultiValuedVariant.from_node_dict(
                        name, value)
        elif 'variants' in node:
            for name, value in node['variants'].items():
                spec.variants[name] = vt.MultiValuedVariant.from_node_dict(
                    name, value
                )
            for name in FlagMap.valid_compiler_flags():
                spec.compiler_flags[name] = []

        spec.external_path = None
        spec.external_modules = None
        if 'external' in node:
            # This conditional is needed because sometimes this function is
            # called with a node already constructed that contains a 'versions'
            # and 'external' field. Related to virtual packages provider
            # indexes.
            if node['external']:
                spec.external_path = node['external']['path']
                spec.external_modules = node['external']['module']
                if spec.external_modules is False:
                    spec.external_modules = None
                spec.extra_attributes = node['external'].get(
                    'extra_attributes', syaml.syaml_dict()
                )

        # specs read in are concrete unless marked abstract
        spec._concrete = node.get('concrete', True)

        # this spec may have been built with older packages than we have
        # on-hand, and we may not have the build dependencies, so mark it
        # so we don't recompute full_hash and build_hash.
        spec._hashes_final = spec._concrete

        if 'patches' in node:
            patches = node['patches']
            if len(patches) > 0:
                mvar = spec.variants.setdefault(
                    'patches', vt.MultiValuedVariant('patches', ())
                )
                mvar.value = patches
                # FIXME: Monkey patches mvar to store patches order
                mvar._patches_in_order_of_appearance = patches

        # Don't read dependencies here; from_node_dict() is used by
        # from_yaml() to read the root *and* each dependency spec.

        return spec

    @staticmethod
    def dependencies_from_node_dict(node):
        name = next(iter(node))
        node = node[name]
        if 'dependencies' not in node:
            return
        for t in Spec.read_yaml_dep_specs(node['dependencies']):
            yield t

    @staticmethod
    def read_yaml_dep_specs(dependency_dict):
        """Read the DependencySpec portion of a YAML-formatted Spec.

        This needs to be backward-compatible with older spack spec
        formats so that reindex will work on old specs/databases.
        """
        for dep_name, elt in dependency_dict.items():
            if isinstance(elt, six.string_types):
                # original format, elt is just the dependency hash.
                dag_hash, deptypes = elt, ['build', 'link']
            elif isinstance(elt, tuple):
                # original deptypes format: (used tuples, not future-proof)
                dag_hash, deptypes = elt
            elif isinstance(elt, dict):
                # new format: elements of dependency spec are keyed.
                dag_hash, deptypes = elt['hash'], elt['type']
            else:
                raise spack.error.SpecError(
                    "Couldn't parse dependency types in spec.")

            yield dep_name, dag_hash, list(deptypes)

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

            def name_and_dependency_types(s):
                """Given a key in the dictionary containing the literal,
                extracts the name of the spec and its dependency types.

                Args:
                    s (str): key in the dictionary containing the literal

                """
                t = s.split(':')

                if len(t) > 2:
                    msg = 'more than one ":" separator in key "{0}"'
                    raise KeyError(msg.format(s))

                n = t[0]
                if len(t) == 2:
                    dtypes = tuple(dt.strip() for dt in t[1].split(','))
                else:
                    dtypes = ()

                return n, dtypes

            def spec_and_dependency_types(s):
                """Given a non-string key in the literal, extracts the spec
                and its dependency types.

                Args:
                    s (spec or tuple): either a Spec object or a tuple
                        composed of a Spec object and a string with the
                        dependency types

                """
                if isinstance(s, Spec):
                    return s, ()

                spec_obj, dtypes = s
                return spec_obj, tuple(dt.strip() for dt in dtypes.split(','))

            # Recurse on dependencies
            for s, s_dependencies in dep_like.items():

                if isinstance(s, six.string_types):
                    dag_node, dependency_types = name_and_dependency_types(s)
                else:
                    dag_node, dependency_types = spec_and_dependency_types(s)

                dependency_spec = spec_builder({dag_node: s_dependencies})
                spec._add_dependency(dependency_spec, dependency_types)

            return spec

        return spec_builder(spec_dict)

    @staticmethod
    def from_dict(data):
        """Construct a spec from YAML.

        Parameters:
        data -- a nested dict/list data structure read from YAML or JSON.
        """
        nodes = data['spec']

        # Read nodes out of list.  Root spec is the first element;
        # dependencies are the following elements.
        dep_list = [Spec.from_node_dict(node) for node in nodes]
        if not dep_list:
            raise spack.error.SpecError("YAML spec contains no nodes.")
        deps = dict((spec.name, spec) for spec in dep_list)
        spec = dep_list[0]

        for node in nodes:
            # get dependency dict from the node.
            name = next(iter(node))

            if 'dependencies' not in node[name]:
                continue

            yaml_deps = node[name]['dependencies']
            for dname, dhash, dtypes in Spec.read_yaml_dep_specs(yaml_deps):
                deps[name]._add_dependency(deps[dname], dtypes)

        return spec

    @staticmethod
    def from_yaml(stream):
        """Construct a spec from YAML.

        Parameters:
        stream -- string or file object to read from.
        """
        try:
            data = yaml.load(stream)
            return Spec.from_dict(data)
        except yaml.error.MarkedYAMLError as e:
            raise syaml.SpackYAMLError("error parsing YAML spec:", str(e))

    @staticmethod
    def from_json(stream):
        """Construct a spec from JSON.

        Parameters:
        stream -- string or file object to read from.
        """
        try:
            data = sjson.load(stream)
            return Spec.from_dict(data)
        except Exception as e:
            tty.debug(e)
            raise sjson.SpackJSONError("error parsing JSON spec:", str(e))

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
        msg = ('cannot validate "{0}" since it was not created '
               'using Spec.from_detection'.format(self))
        assert isinstance(self.extra_attributes, Mapping), msg

        # Validate the spec calling a package specific method
        validate_fn = getattr(
            self.package, 'validate_detected_spec', lambda x, y: None
        )
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
        for name in sorted(self._dependencies.keys()):
            changed |= self._dependencies[name].spec._concretize_helper(
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
                    (concretizer.concretize_develop(self),  # special variant
                     concretizer.concretize_architecture(self),
                     concretizer.concretize_compiler(self),
                     concretizer.adjust_target(self),
                     # flags must be concretized after compiler
                     concretizer.concretize_compiler_flags(self),
                     concretizer.concretize_version(self),
                     concretizer.concretize_variants(self)))
            presets[self.name] = self

        visited.add(self.name)
        return changed

    def _replace_with(self, concrete):
        """Replace this virtual spec with a concrete spec."""
        assert(self.virtual)
        for name, dep_spec in self._dependents.items():
            dependent = dep_spec.parent
            deptypes = dep_spec.deptypes

            # remove self from all dependents, unless it is already removed
            if self.name in dependent._dependencies:
                del dependent._dependencies[self.name]

            # add the replacement, unless it is already a dep of dependent.
            if concrete.name not in dependent._dependencies:
                dependent._add_dependency(concrete, deptypes)

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
            self.traverse(), restrict=True)
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
                    if (spec._dependencies):
                        for dep in spec.dependencies():
                            del dep._dependents[spec.name]
                        changed = True
                        spec._dependencies = DependencyMap()
                    replacement._dependencies = DependencyMap()
                    replacement.architecture = self.architecture

                # TODO: could this and the stuff in _dup be cleaned up?
                def feq(cfield, sfield):
                    return (not cfield) or (cfield == sfield)

                if replacement is spec or (
                        feq(replacement.name, spec.name) and
                        feq(replacement.versions, spec.versions) and
                        feq(replacement.compiler, spec.compiler) and
                        feq(replacement.architecture, spec.architecture) and
                        feq(replacement._dependencies, spec._dependencies) and
                        feq(replacement.variants, spec.variants) and
                        feq(replacement.external_path,
                            spec.external_path) and
                        feq(replacement.external_modules,
                            spec.external_modules)):
                    continue
                # Refine this spec to the candidate. This uses
                # replace_with AND dup so that it can work in
                # place. TODO: make this more efficient.
                if spec.virtual:
                    spec._replace_with(replacement)
                    changed = True
                if spec._dup(replacement, deps=False, cleardeps=False):
                    changed = True

                spec._dependencies.owner = spec
                self_index.update(spec)
                done = False
                break

        return changed

    def _old_concretize(self, tests=False):
        """A spec is concrete if it describes one build of a package uniquely.
        This will ensure that this spec is concrete.

        Args:
            tests (list or bool): list of packages that will need test
                dependencies, or True/False for test all/none

        If this spec could describe more than one version, variant, or build
        of a package, this will add constraints to make it concrete.

        Some rigorous validation and checks are also performed on the spec.
        Concretizing ensures that it is self-consistent and that it's
        consistent with requirements of its packages. See flatten() and
        normalize() for more details on this.
        """
        import spack.concretize

        if not self.name:
            raise spack.error.SpecError(
                "Attempting to concretize anonymous spec")

        if self._concrete:
            return

        changed = True
        force = False

        user_spec_deps = self.flat_dependencies(copy=False)
        concretizer = spack.concretize.Concretizer(self.copy())
        while changed:
            changes = (self.normalize(force, tests=tests,
                                      user_spec_deps=user_spec_deps),
                       self._expand_virtual_packages(concretizer),
                       self._concretize_helper(concretizer))
            changed = any(changes)
            force = True

        visited_user_specs = set()
        for dep in self.traverse():
            visited_user_specs.add(dep.name)
            visited_user_specs.update(x.name for x in dep.package.provided)

        extra = set(user_spec_deps.keys()).difference(visited_user_specs)
        if extra:
            raise InvalidDependencyError(self.name, extra)

        Spec.inject_patches_variant(self)

        for s in self.traverse():
            # TODO: Refactor this into a common method to build external specs
            # TODO: or turn external_path into a lazy property
            Spec.ensure_external_path_if_external(s)

        # Mark everything in the spec as concrete, as well.
        self._mark_concrete()

        # If any spec in the DAG is deprecated, throw an error
        Spec.ensure_no_deprecated(self)

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
            for conflict_spec, when_list in x.package_class.conflicts.items():
                if x.satisfies(conflict_spec, strict=True):
                    for when_spec, msg in when_list:
                        if x.satisfies(when_spec, strict=True):
                            when = when_spec.copy()
                            when.name = x.name
                            matches.append((x, conflict_spec, when, msg))
        if matches:
            raise ConflictsInSpecError(self, matches)

        # Check if we can produce an optimized binary (will throw if
        # there are declared inconsistencies)
        self.architecture.target.optimization_flags(self.compiler)

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
                s.namespace = spack.repo.path.repo_for_pkg(s.name).namespace

            if s.concrete:
                continue

            # Add any patches from the package to the spec.
            patches = []
            for cond, patch_list in s.package_class.patches.items():
                if s.satisfies(cond, strict=True):
                    for patch in patch_list:
                        patches.append(patch)
            if patches:
                spec_to_patches[id(s)] = patches
        # Also record all patches required on dependencies by
        # depends_on(..., patch=...)
        for dspec in root.traverse_edges(deptype=all,
                                         cover='edges', root=False):
            pkg_deps = dspec.parent.package_class.dependencies
            if dspec.spec.name not in pkg_deps:
                continue

            if dspec.spec.concrete:
                continue

            patches = []
            for cond, dependency in pkg_deps[dspec.spec.name].items():
                for pcond, patch_list in dependency.patches.items():
                    if (dspec.parent.satisfies(cond, strict=True)
                            and dspec.spec.satisfies(pcond)):
                        patches.extend(patch_list)
            if patches:
                all_patches = spec_to_patches.setdefault(id(dspec.spec), [])
                all_patches.extend(patches)
        for spec in root.traverse():
            if id(spec) not in spec_to_patches:
                continue

            patches = list(lang.dedupe(spec_to_patches[id(spec)]))
            mvar = spec.variants.setdefault(
                'patches', vt.MultiValuedVariant('patches', ())
            )
            mvar.value = tuple(p.sha256 for p in patches)
            # FIXME: Monkey patches mvar to store patches order
            full_order_keys = list(tuple(p.ordering_key) + (p.sha256,) for p
                                   in patches)
            ordered_hashes = sorted(full_order_keys)
            tty.debug("Ordered hashes [{0}]: ".format(spec.name) +
                      ', '.join('/'.join(str(e) for e in t)
                                for t in ordered_hashes))
            mvar._patches_in_order_of_appearance = list(
                t[-1] for t in ordered_hashes)

    @staticmethod
    def ensure_external_path_if_external(external_spec):
        if external_spec.external_modules and not external_spec.external_path:
            compiler = spack.compilers.compiler_for_spec(
                external_spec.compiler, external_spec.architecture)
            for mod in compiler.modules:
                md.load_module(mod)

            # get the path from the module
            # the package can override the default
            external_spec.external_path = getattr(
                external_spec.package, 'external_prefix',
                md.path_from_modules(external_spec.external_modules)
            )

    @staticmethod
    def ensure_no_deprecated(root):
        """Raise is a deprecated spec is in the dag.

        Args:
            root (Spec): root spec to be analyzed

        Raises:
            SpecDeprecatedError: is any deprecated spec is found
        """
        deprecated = []
        with spack.store.db.read_transaction():
            for x in root.traverse():
                _, rec = spack.store.db.query_by_spec_hash(x.dag_hash())
                if rec and rec.deprecated_for:
                    deprecated.append(rec)
        if deprecated:
            msg = "\n    The following specs have been deprecated"
            msg += " in favor of specs with the hashes shown:\n"
            for rec in deprecated:
                msg += '        %s  --> %s\n' % (rec.spec, rec.deprecated_for)
            msg += '\n'
            msg += "    For each package listed, choose another spec\n"
            raise SpecDeprecatedError(msg)

    def _new_concretize(self, tests=False):
        import spack.solver.asp

        if not self.name:
            raise spack.error.SpecError(
                "Spec has no name; cannot concretize an anonymous spec")

        if self._concrete:
            return

        result = spack.solver.asp.solve([self], tests=tests)
        if not result.satisfiable:
            result.print_cores()
            raise spack.error.UnsatisfiableSpecError(
                self, "unknown", "Unsatisfiable!")

        # take the best answer
        opt, i, answer = min(result.answers)
        name = self.name
        # TODO: Consolidate this code with similar code in solve.py
        if self.virtual:
            providers = [spec.name for spec in answer.values()
                         if spec.package.provides(name)]
            name = providers[0]

        assert name in answer

        concretized = answer[name]
        self._dup(concretized)
        self._mark_concrete()

    def concretize(self, tests=False):
        """Concretize the current spec.

        Args:
            tests (bool or list): if False disregard 'test' dependencies,
                if a list of names activate them for the packages in the list,
                if True activate 'test' dependencies for all packages.
        """
        if spack.config.get('config:concretizer') == "clingo":
            self._new_concretize(tests)
        else:
            self._old_concretize(tests)

    def _mark_root_concrete(self, value=True):
        """Mark just this spec (not dependencies) concrete."""
        if (not value) and self.concrete and self.package.installed:
            return
        self._normal = value
        self._concrete = value

    def _mark_concrete(self, value=True):
        """Mark this spec and its dependencies as concrete.

        Only for internal use -- client code should use "concretize"
        unless there is a need to force a spec to be concrete.
        """
        # if set to false, clear out all hashes (set to None or remove attr)
        # may need to change references to respect None
        for s in self.traverse():
            if (not value) and s.concrete and s.package.installed:
                continue
            elif not value:
                s.clear_cached_hashes()
            s._mark_root_concrete(value)

    def concretized(self, tests=False):
        """This is a non-destructive version of concretize().

        First clones, then returns a concrete version of this package
        without modifying this package.

        Args:
            tests (bool or list): if False disregard 'test' dependencies,
                if a list of names activate them for the packages in the list,
                if True activate 'test' dependencies for all packages.
        """
        clone = self.copy(caches=False)
        clone.concretize(tests=tests)
        return clone

    def flat_dependencies(self, **kwargs):
        """Return a DependencyMap containing all of this spec's
           dependencies with their constraints merged.

           If copy is True, returns merged copies of its dependencies
           without modifying the spec it's called on.

           If copy is False, clears this spec's dependencies and
           returns them. This disconnects all dependency links including
           transitive dependencies, except for concrete specs: if a spec
           is concrete it will not be disconnected from its dependencies
           (although a non-concrete spec with concrete dependencies will
           be disconnected from those dependencies).
        """
        copy = kwargs.get('copy', True)

        flat_deps = {}
        try:
            deptree = self.traverse(root=False)
            for spec in deptree:

                if spec.name not in flat_deps:
                    if copy:
                        spec = spec.copy(deps=False)
                    flat_deps[spec.name] = spec
                else:
                    flat_deps[spec.name].constrain(spec)

            if not copy:
                for spec in flat_deps.values():
                    if not spec.concrete:
                        spec._dependencies.clear()
                        spec._dependents.clear()
                self._dependencies.clear()

            return flat_deps

        except spack.error.UnsatisfiableSpecError as e:
            # Here, the DAG contains two instances of the same package
            # with inconsistent constraints.  Users cannot produce
            # inconsistent specs like this on the command line: the
            # parser doesn't allow it. Spack must be broken!
            raise InconsistentSpecError("Invalid Spec DAG: %s" % e.message)

    def index(self, deptype='all'):
        """Return DependencyMap that points to all the dependencies in this
           spec."""
        dm = DependencyMap()
        for spec in self.traverse(deptype=deptype):
            dm[spec.name] = spec
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
        conditions = self.package_class.dependencies[name]

        vt.substitute_abstract_variants(self)
        # evaluate when specs to figure out constraints on the dependency.
        dep = None
        for when_spec, dependency in conditions.items():
            if self.satisfies(when_spec, strict=True):
                if dep is None:
                    dep = dp.Dependency(self.name, Spec(name), type=())
                try:
                    dep.merge(dependency)
                except spack.error.UnsatisfiableSpecError as e:
                    e.message = (
                        "Conflicting conditional dependencies for spec"
                        "\n\n\t{0}\n\n"
                        "Cannot merge constraint"
                        "\n\n\t{1}\n\n"
                        "into"
                        "\n\n\t{2}"
                        .format(self, dependency.spec, dep.spec))
                    raise e

        return dep

    def _find_provider(self, vdep, provider_index):
        """Find provider for a virtual spec in the provider index.
           Raise an exception if there is a conflicting virtual
           dependency already in this spec.
        """
        assert(vdep.virtual)

        # note that this defensively copies.
        providers = provider_index.providers_for(vdep)

        # If there is a provider for the vpkg, then use that instead of
        # the virtual package.
        if providers:
            # Remove duplicate providers that can concretize to the same
            # result.
            for provider in providers:
                for spec in providers:
                    if spec is not provider and provider.satisfies(spec):
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

    def _merge_dependency(
            self, dependency, visited, spec_deps, provider_index, tests):
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
        if dep.virtual:
            visited.add(dep.name)
            provider = self._find_provider(dep, provider_index)
            if provider:
                dep = provider
        else:
            index = spack.provider_index.ProviderIndex([dep], restrict=True)
            items = list(spec_deps.items())
            for name, vspec in items:
                if not vspec.virtual:
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
                tty.debug(
                    "{0} applying constraint {1}".format(self.name, str(dep)))
                changed |= spec_deps[dep.name].constrain(dep)
            except spack.error.UnsatisfiableSpecError as e:
                fmt = 'An unsatisfiable {0}'.format(e.constraint_type)
                fmt += ' constraint has been detected for spec:'
                fmt += '\n\n{0}\n\n'.format(spec_deps[dep.name].tree(indent=4))
                fmt += 'while trying to concretize the partial spec:'
                fmt += '\n\n{0}\n\n'.format(self.tree(indent=4))
                fmt += '{0} requires {1} {2} {3}, but spec asked for {4}'

                e.message = fmt.format(
                    self.name,
                    dep.name,
                    e.constraint_type,
                    e.required,
                    e.provided)

                raise

        # Add merged spec to my deps and recurse
        spec_dependency = spec_deps[dep.name]
        if dep.name not in self._dependencies:
            self._add_dependency(spec_dependency, dependency.type)

        changed |= spec_dependency._normalize_helper(
            visited, spec_deps, provider_index, tests)
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
        if self.concrete and self.package.installed:
            return False

        # Combine constraints from package deps with constraints from
        # the spec, until nothing changes.
        any_change = False
        changed = True

        while changed:
            changed = False
            for dep_name in self.package_class.dependencies:
                # Do we depend on dep_name?  If so pkg_dep is not None.
                dep = self._evaluate_dependency_conditions(dep_name)

                # If dep is a needed dependency, merge it.
                if dep:
                    merge = (
                        # caller requested test dependencies
                        tests is True or (tests and self.name in tests) or
                        # this is not a test-only dependency
                        dep.type - set(['test']))

                    if merge:
                        changed |= self._merge_dependency(
                            dep, visited, spec_deps, provider_index, tests)
            any_change |= changed

        return any_change

    def normalize(self, force=False, tests=False, user_spec_deps=None):
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
            raise spack.error.SpecError(
                "Attempting to normalize anonymous spec")

        # Set _normal and _concrete to False when forced
        if force:
            self._mark_concrete(False)

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
        all_spec_deps = self.flat_dependencies(copy=False)

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
            [s for s in all_spec_deps.values()], restrict=True)

        # traverse the package DAG and fill out dependencies according
        # to package files & their 'when' specs
        visited = set()

        any_change = self._normalize_helper(
            visited, all_spec_deps, provider_index, tests)

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
                spack.repo.get(spec.fullname)

            # validate compiler in addition to the package name.
            if spec.compiler:
                if not compilers.supported(spec.compiler):
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
            UnknownVariantError: on the first unknown variant found
        """
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

        pkg_variant = self.package_class.variants[variant_name]

        for value in values:
            if self.variants.get(variant_name):
                msg = ("Cannot append a value to a single-valued "
                       "variant with an already set value")
                assert pkg_variant.multi, msg
                self.variants[variant_name].append(value)
            else:
                variant = pkg_variant.make_variant(value)
                self.variants[variant_name] = variant

        pkg_variant.validate_or_raise(
            self.variants[variant_name], self.package)

    def constrain(self, other, deps=True):
        """Merge the constraints of other with self.

        Returns True if the spec changed as a result, False if not.
        """
        # If we are trying to constrain a concrete spec, either the spec
        # already satisfies the constraint (and the method returns False)
        # or it raises an exception
        if self.concrete:
            if self.satisfies(other):
                return False
            else:
                raise spack.error.UnsatisfiableSpecError(
                    self, other, 'constrain a concrete spec'
                )

        other = self._autospec(other)

        if not (self.name == other.name or
                (not self.name) or
                (not other.name)):
            raise UnsatisfiableSpecNameError(self.name, other.name)

        if (other.namespace is not None and
                self.namespace is not None and
                other.namespace != self.namespace):
            raise UnsatisfiableSpecNameError(self.fullname, other.fullname)

        if not self.versions.overlaps(other.versions):
            raise UnsatisfiableVersionSpecError(self.versions, other.versions)

        for v in [x for x in other.variants if x in self.variants]:
            if not self.variants[v].compatible(other.variants[v]):
                raise vt.UnsatisfiableVariantSpecError(
                    self.variants[v], other.variants[v]
                )

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
        if self.compiler is not None and other.compiler is not None:
            changed |= self.compiler.constrain(other.compiler)
        elif self.compiler is None:
            changed |= (self.compiler != other.compiler)
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
        changed |= (str(self.architecture) != old)

        if deps:
            changed |= self._constrain_dependencies(other)

        return changed

    def _constrain_dependencies(self, other):
        """Apply constraints of other spec's dependencies to this spec."""
        other = self._autospec(other)

        if not other._dependencies:
            return False

        # TODO: might want more detail than this, e.g. specific deps
        # in violation. if this becomes a priority get rid of this
        # check and be more specific about what's wrong.
        if not other.satisfies_dependencies(self):
            raise UnsatisfiableDependencySpecError(other, self)

        if any(not d.name for d in other.traverse(root=False)):
            raise UnconstrainableDependencySpecError(other)

        # Handle common first-order constraints directly
        changed = False
        for name in self.common_dependencies(other):
            changed |= self[name].constrain(other[name], deps=False)
            if name in self._dependencies:
                changed |= self._dependencies[name].update_deptypes(
                    other._dependencies[name].deptypes)

        # Update with additional constraints from other spec
        for name in other.dep_difference(self):
            dep_spec_copy = other.get_dependency(name)
            dep_copy = dep_spec_copy.spec
            deptypes = dep_spec_copy.deptypes
            self._add_dependency(dep_copy.copy(), deptypes)
            changed = True

        return changed

    def common_dependencies(self, other):
        """Return names of dependencies that self an other have in common."""
        common = set(
            s.name for s in self.traverse(root=False))
        common.intersection_update(
            s.name for s in other.traverse(root=False))
        return common

    def constrained(self, other, deps=True):
        """Return a constrained copy without modifying this spec."""
        clone = self.copy(deps=deps)
        clone.constrain(other, deps)
        return clone

    def dep_difference(self, other):
        """Returns dependencies in self that are not in other."""
        mine = set(s.name for s in self.traverse(root=False))
        mine.difference_update(
            s.name for s in other.traverse(root=False))
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

    def satisfies(self, other, deps=True, strict=False, strict_deps=False):
        """Determine if this spec satisfies all constraints of another.

        There are two senses for satisfies:

          * `loose` (default): the absence of a constraint in self
            implies that it *could* be satisfied by other, so we only
            check that there are no conflicts with other for
            constraints that this spec actually has.

          * `strict`: strict means that we *must* meet all the
            constraints specified on other.
        """
        other = self._autospec(other)

        # The only way to satisfy a concrete spec is to match its hash exactly.
        if other.concrete:
            return self.concrete and self.dag_hash() == other.dag_hash()

        # A concrete provider can satisfy a virtual dependency.
        if not self.virtual and other.virtual:
            try:
                pkg = spack.repo.get(self.fullname)
            except spack.repo.UnknownEntityError:
                # If we can't get package info on this spec, don't treat
                # it as a provider of this vdep.
                return False

            if pkg.provides(other.name):
                for provided, when_specs in pkg.provided.items():
                    if any(self.satisfies(when_spec, deps=False, strict=strict)
                           for when_spec in when_specs):
                        if provided.satisfies(other):
                            return True
            return False

        # Otherwise, first thing we care about is whether the name matches
        if self.name != other.name and self.name and other.name:
            return False

        # namespaces either match, or other doesn't require one.
        if (other.namespace is not None and
                self.namespace is not None and
                self.namespace != other.namespace):
            return False
        if self.versions and other.versions:
            if not self.versions.satisfies(other.versions, strict=strict):
                return False
        elif strict and (self.versions or other.versions):
            return False

        # None indicates no constraints when not strict.
        if self.compiler and other.compiler:
            if not self.compiler.satisfies(other.compiler, strict=strict):
                return False
        elif strict and (other.compiler and not self.compiler):
            return False

        var_strict = strict
        if (not self.name) or (not other.name):
            var_strict = True
        if not self.variants.satisfies(other.variants, strict=var_strict):
            return False

        # Architecture satisfaction is currently just string equality.
        # If not strict, None means unconstrained.
        if self.architecture and other.architecture:
            if not self.architecture.satisfies(other.architecture, strict):
                return False
        elif strict and (other.architecture and not self.architecture):
            return False

        if not self.compiler_flags.satisfies(
                other.compiler_flags,
                strict=strict):
            return False

        # If we need to descend into dependencies, do it, otherwise we're done.
        if deps:
            deps_strict = strict
            if self._concrete and not other.name:
                # We're dealing with existing specs
                deps_strict = True
            return self.satisfies_dependencies(other, strict=deps_strict)
        else:
            return True

    def satisfies_dependencies(self, other, strict=False):
        """
        This checks constraints on common dependencies against each other.
        """
        other = self._autospec(other)

        # If there are no constraints to satisfy, we're done.
        if not other._dependencies:
            return True

        if strict:
            # if we have no dependencies, we can't satisfy any constraints.
            if not self._dependencies:
                return False

            # use list to prevent double-iteration
            selfdeps = list(self.traverse(root=False))
            otherdeps = list(other.traverse(root=False))
            if not all(any(d.satisfies(dep, strict=True) for d in selfdeps)
                       for dep in otherdeps):
                return False

        elif not self._dependencies:
            # if not strict, this spec *could* eventually satisfy the
            # constraints on other.
            return True

        # Handle first-order constraints directly
        for name in self.common_dependencies(other):
            if not self[name].satisfies(other[name], deps=False):
                return False

        # For virtual dependencies, we need to dig a little deeper.
        self_index = spack.provider_index.ProviderIndex(
            self.traverse(), restrict=True)
        other_index = spack.provider_index.ProviderIndex(
            other.traverse(), restrict=True)

        # This handles cases where there are already providers for both vpkgs
        if not self_index.satisfies(other_index):
            return False

        # These two loops handle cases where there is an overly restrictive
        # vpkg in one spec for a provider in the other (e.g., mpi@3: is not
        # compatible with mpich2)
        for spec in self.virtual_dependencies():
            if (spec.name in other_index and
                    not other_index.providers_for(spec)):
                return False

        for spec in other.virtual_dependencies():
            if spec.name in self_index and not self_index.providers_for(spec):
                return False

        return True

    def virtual_dependencies(self):
        """Return list of any virtual deps in this spec."""
        return [spec for spec in self.traverse() if spec.virtual]

    @property  # type: ignore[misc] # decorated prop not supported in mypy
    @lang.memoized
    def patches(self):
        """Return patch objects for any patch sha256 sums on this Spec.

        This is for use after concretization to iterate over any patches
        associated with this spec.

        TODO: this only checks in the package; it doesn't resurrect old
        patches from install directories, but it probably should.
        """
        if not self.concrete:
            raise spack.error.SpecError("Spec is not concrete: " + str(self))

        if 'patches' not in self.variants:
            return []

        # FIXME: _patches_in_order_of_appearance is attached after
        # FIXME: concretization to store the order of patches somewhere.
        # FIXME: Needs to be refactored in a cleaner way.

        # translate patch sha256sums to patch objects by consulting the index
        patches = []
        for sha256 in self.variants['patches']._patches_in_order_of_appearance:
            index = spack.repo.path.patch_index
            patch = index.patch_for_package(sha256, self.package)
            patches.append(patch)

        return patches

    def _dup(self, other, deps=True, cleardeps=True, caches=None):
        """Copy the spec other into self.  This is an overwriting
        copy. It does not copy any dependents (parents), but by default
        copies dependencies.

        To duplicate an entire DAG, call _dup() on the root of the DAG.

        Args:
            other (Spec): spec to be copied onto ``self``
            deps (bool or Sequence): if True copies all the dependencies. If
                False copies None. If a sequence of dependency types copy
                only those types.
            cleardeps (bool): if True clears the dependencies of ``self``,
                before possibly copying the dependencies of ``other`` onto
                ``self``
            caches (bool or None): preserve cached fields such as
                ``_normal``, ``_hash``, and ``_cmp_key_cache``. By
                default this is ``False`` if DAG structure would be
                changed by the copy, ``True`` if it's an exact copy.

        Returns:
            True if ``self`` changed because of the copy operation,
            False otherwise.

        """
        # We don't count dependencies as changes here
        changed = True
        if hasattr(self, 'name'):
            changed = (self.name != other.name and
                       self.versions != other.versions and
                       self.architecture != other.architecture and
                       self.compiler != other.compiler and
                       self.variants != other.variants and
                       self._normal != other._normal and
                       self.concrete != other.concrete and
                       self.external_path != other.external_path and
                       self.external_modules != other.external_modules and
                       self.compiler_flags != other.compiler_flags)

        self._package = None

        # Local node attributes get copied first.
        self.name = other.name
        self.versions = other.versions.copy()
        self.architecture = other.architecture.copy() if other.architecture \
            else None
        self.compiler = other.compiler.copy() if other.compiler else None
        if cleardeps:
            self._dependents = DependencyMap()
            self._dependencies = DependencyMap()
        self.compiler_flags = other.compiler_flags.copy()
        self.compiler_flags.spec = self
        self.variants = other.variants.copy()
        self._build_spec = other._build_spec

        # FIXME: we manage _patches_in_order_of_appearance specially here
        # to keep it from leaking out of spec.py, but we should figure
        # out how to handle it more elegantly in the Variant classes.
        for k, v in other.variants.items():
            patches = getattr(v, '_patches_in_order_of_appearance', None)
            if patches:
                self.variants[k]._patches_in_order_of_appearance = patches

        self.variants.spec = self
        self.external_path = other.external_path
        self.external_modules = other.external_modules
        self.extra_attributes = other.extra_attributes
        self.namespace = other.namespace

        # Cached fields are results of expensive operations.
        # If we preserved the original structure, we can copy them
        # safely. If not, they need to be recomputed.
        if caches is None:
            caches = (deps is True or deps == dp.all_deptypes)

        # If we copy dependencies, preserve DAG structure in the new spec
        if deps:
            # If caller restricted deptypes to be copied, adjust that here.
            # By default, just copy all deptypes
            deptypes = dp.all_deptypes
            if isinstance(deps, (tuple, list)):
                deptypes = deps
            self._dup_deps(other, deptypes, caches)

        self._concrete = other._concrete
        self._hashes_final = other._hashes_final

        if caches:
            self._hash = other._hash
            self._build_hash = other._build_hash
            self._cmp_key_cache = other._cmp_key_cache
            self._normal = other._normal
            self._full_hash = other._full_hash
        else:
            self._hash = None
            self._build_hash = None
            self._cmp_key_cache = None
            self._normal = False
            self._full_hash = None

        return changed

    def _dup_deps(self, other, deptypes, caches):
        new_specs = {self.name: self}
        for dspec in other.traverse_edges(cover='edges',
                                          root=False):
            if (dspec.deptypes and
                not any(d in deptypes for d in dspec.deptypes)):
                continue

            if dspec.parent.name not in new_specs:
                new_specs[dspec.parent.name] = dspec.parent.copy(
                    deps=False, caches=caches)
            if dspec.spec.name not in new_specs:
                new_specs[dspec.spec.name] = dspec.spec.copy(
                    deps=False, caches=caches)

            new_specs[dspec.parent.name]._add_dependency(
                new_specs[dspec.spec.name], dspec.deptypes)

    def copy(self, deps=True, **kwargs):
        """Make a copy of this spec.

        Args:
            deps (bool or tuple): Defaults to True. If boolean, controls
                whether dependencies are copied (copied if True). If a
                tuple is provided, *only* dependencies of types matching
                those in the tuple are copied.
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
            raise spack.error.SpecError(
                "Spec version is not concrete: " + str(self))
        return self.versions[0]

    def __getitem__(self, name):
        """Get a dependency from the spec by its name. This call implicitly
        sets a query state in the package being retrieved. The behavior of
        packages may be influenced by additional query parameters that are
        passed after a colon symbol.

        Note that if a virtual package is queried a copy of the Spec is
        returned while for non-virtual a reference is returned.
        """
        query_parameters = name.split(':')
        if len(query_parameters) > 2:
            msg = 'key has more than one \':\' symbol.'
            msg += ' At most one is admitted.'
            raise KeyError(msg)

        name, query_parameters = query_parameters[0], query_parameters[1:]
        if query_parameters:
            # We have extra query parameters, which are comma separated
            # values
            csv = query_parameters.pop().strip()
            query_parameters = re.split(r'\s*,\s*', csv)

        try:
            value = next(
                itertools.chain(
                    # Regular specs
                    (x for x in self.traverse() if x.name == name),
                    (x for x in self.traverse()
                     if (not x.virtual) and x.package.provides(name))
                )
            )
        except StopIteration:
            raise KeyError("No spec with name %s in %s" % (name, self))

        if self._concrete:
            return SpecBuildInterface(value, name, query_parameters)

        return value

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

    def sorted_deps(self):
        """Return a list of all dependencies sorted by name."""
        deps = self.flat_dependencies()
        return tuple(deps[name] for name in sorted(deps))

    def _eq_dag(self, other, vs, vo, deptypes):
        """Recursive helper for eq_dag and ne_dag.  Does the actual DAG
           traversal."""
        vs.add(id(self))
        vo.add(id(other))

        if self.ne_node(other):
            return False

        if len(self._dependencies) != len(other._dependencies):
            return False

        ssorted = [self._dependencies[name]
                   for name in sorted(self._dependencies)]
        osorted = [other._dependencies[name]
                   for name in sorted(other._dependencies)]

        for s_dspec, o_dspec in zip(ssorted, osorted):
            if deptypes and s_dspec.deptypes != o_dspec.deptypes:
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
            if not s._eq_dag(o, vs, vo, deptypes):
                return False

        return True

    def eq_dag(self, other, deptypes=True):
        """True if the full dependency DAGs of specs are equal."""
        return self._eq_dag(other, set(), set(), deptypes)

    def ne_dag(self, other, deptypes=True):
        """True if the full dependency DAGs of specs are not equal."""
        return not self.eq_dag(other, set(), set(), deptypes)

    def _cmp_node(self):
        """Comparison key for just *this node* and not its deps."""
        # Name or namespace None will lead to invalid comparisons for abstract
        # specs. Replace them with the empty string, which is not a valid spec
        # name nor namespace so it will not create spurious equalities.
        return (self.name or '',
                self.namespace or '',
                tuple(self.versions),
                self.variants,
                self.architecture,
                self.compiler,
                self.compiler_flags)

    def eq_node(self, other):
        """Equality with another spec, not including dependencies."""
        return self._cmp_node() == other._cmp_node()

    def ne_node(self, other):
        """Inequality with another spec, not including dependencies."""
        return self._cmp_node() != other._cmp_node()

    def _cmp_key(self):
        """This returns a key for the spec *including* DAG structure.

        The key is the concatenation of:
          1. A tuple describing this node in the DAG.
          2. The hash of each of this node's dependencies' cmp_keys.
        """
        if self._cmp_key_cache:
            return self._cmp_key_cache

        dep_tuple = tuple(
            (d.spec.name, hash(d.spec), tuple(sorted(d.deptypes)))
            for name, d in sorted(self._dependencies.items()))

        key = (self._cmp_node(), dep_tuple)
        if self._concrete:
            self._cmp_key_cache = key
        return key

    def colorized(self):
        return colorize_spec(self)

    def format(self, format_string=default_format, **kwargs):
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
        literal ``\`` character. Also use ``\$`` for the literal ``$``
        to differentiate from previous, deprecated format string
        syntax.

        The previous format strings are deprecated. They can still be
        accessed by the ``old_format`` method. The ``format`` method
        will call ``old_format`` if the character ``$`` appears
        unescaped in the format string.


        Args:
            format_string (str): string containing the format to be expanded

        Keyword Args:
            color (bool): True if returned string is colored
            transform (dict): maps full-string formats to a callable \
                that accepts a string and returns another one

        """
        # If we have an unescaped $ sigil, use the deprecated format strings
        if re.search(r'[^\\]*\$', format_string):
            return self.old_format(format_string, **kwargs)

        color = kwargs.get('color', False)
        transform = kwargs.get('transform', {})

        out = six.StringIO()

        def write(s, c=None):
            f = clr.cescape(s)
            if c is not None:
                f = color_formats[c] + f + '@.'
            clr.cwrite(f, stream=out, color=color)

        def write_attribute(spec, attribute, color):
            current = spec
            if attribute.startswith('^'):
                attribute = attribute[1:]
                dep, attribute = attribute.split('.', 1)
                current = self[dep]

            if attribute == '':
                raise SpecFormatStringError(
                    'Format string attributes must be non-empty')
            attribute = attribute.lower()

            sig = ''
            if attribute[0] in '@%/':
                # color sigils that are inside braces
                sig = attribute[0]
                attribute = attribute[1:]
            elif attribute.startswith('arch='):
                sig = ' arch='  # include space as separator
                attribute = attribute[5:]

            parts = attribute.split('.')
            assert parts

            # check that the sigil is valid for the attribute.
            if sig == '@' and parts[-1] not in ('versions', 'version'):
                raise SpecFormatSigilError(sig, 'versions', attribute)
            elif sig == '%' and attribute not in ('compiler', 'compiler.name'):
                raise SpecFormatSigilError(sig, 'compilers', attribute)
            elif sig == '/' and not re.match(r'hash(:\d+)?$', attribute):
                raise SpecFormatSigilError(sig, 'DAG hashes', attribute)
            elif sig == ' arch=' and attribute not in ('architecture', 'arch'):
                raise SpecFormatSigilError(sig, 'the architecture', attribute)

            # find the morph function for our attribute
            morph = transform.get(attribute, lambda s, x: x)

            # Special cases for non-spec attributes and hashes.
            # These must be the only non-dep component of the format attribute
            if attribute == 'spack_root':
                write(morph(spec, spack.paths.spack_root))
                return
            elif attribute == 'spack_install':
                write(morph(spec, spack.store.layout.root))
                return
            elif re.match(r'hash(:\d)?', attribute):
                col = '#'
                if ':' in attribute:
                    _, length = attribute.split(':')
                    write(sig + morph(spec, spec.dag_hash(int(length))), col)
                else:
                    write(sig + morph(spec, spec.dag_hash()), col)
                return

            # Iterate over components using getattr to get next element
            for idx, part in enumerate(parts):
                if not part:
                    raise SpecFormatStringError(
                        'Format string attributes must be non-empty'
                    )
                if part.startswith('_'):
                    raise SpecFormatStringError(
                        'Attempted to format private attribute'
                    )
                else:
                    if isinstance(current, vt.VariantMap):
                        # subscript instead of getattr for variant names
                        current = current[part]
                    else:
                        # aliases
                        if part == 'arch':
                            part = 'architecture'
                        elif part == 'version':
                            # Version requires concrete spec, versions does not
                            # when concrete, they print the same thing
                            part = 'versions'
                        try:
                            current = getattr(current, part)
                        except AttributeError:
                            parent = '.'.join(parts[:idx])
                            m = 'Attempted to format attribute %s.' % attribute
                            m += 'Spec.%s has no attribute %s' % (parent, part)
                            raise SpecFormatStringError(m)
                        if isinstance(current, vn.VersionList):
                            if current == _any_version:
                                # We don't print empty version lists
                                return

                    if callable(current):
                        raise SpecFormatStringError(
                            'Attempted to format callable object'
                        )
                    if not current:
                        # We're not printing anything
                        return

            # Set color codes for various attributes
            col = None
            if 'variants' in parts:
                col = '+'
            elif 'architecture' in parts:
                col = '='
            elif 'compiler' in parts or 'compiler_flags' in parts:
                col = '%'
            elif 'version' in parts:
                col = '@'

            # Finally, write the ouptut
            write(sig + morph(spec, str(current)), col)

        attribute = ''
        in_attribute = False
        escape = False

        for c in format_string:
            if escape:
                out.write(c)
                escape = False
            elif c == '\\':
                escape = True
            elif in_attribute:
                if c == '}':
                    write_attribute(self, attribute, color)
                    attribute = ''
                    in_attribute = False
                else:
                    attribute += c
            else:
                if c == '}':
                    raise SpecFormatStringError(
                        'Encountered closing } before opening {'
                    )
                elif c == '{':
                    in_attribute = True
                else:
                    out.write(c)
        if in_attribute:
            raise SpecFormatStringError(
                'Format string terminated while reading attribute.'
                'Missing terminating }.'
            )
        return out.getvalue()

    def old_format(self, format_string='$_$@$%@+$+$=', **kwargs):
        """
        The format strings you can provide are::

            $_   Package name
            $.   Full package name (with namespace)
            $@   Version with '@' prefix
            $%   Compiler with '%' prefix
            $%@  Compiler with '%' prefix & compiler version with '@' prefix
            $%+  Compiler with '%' prefix & compiler flags prefixed by name
            $%@+ Compiler, compiler version, and compiler flags with same
                 prefixes as above
            $+   Options
            $=   Architecture prefixed by 'arch='
            $/   7-char prefix of DAG hash with '-' prefix
            $$   $

        You can also use full-string versions, which elide the prefixes::

            ${PACKAGE}       Package name
            ${FULLPACKAGE}   Full package name (with namespace)
            ${VERSION}       Version
            ${COMPILER}      Full compiler string
            ${COMPILERNAME}  Compiler name
            ${COMPILERVER}   Compiler version
            ${COMPILERFLAGS} Compiler flags
            ${OPTIONS}       Options
            ${ARCHITECTURE}  Architecture
            ${PLATFORM}      Platform
            ${OS}            Operating System
            ${TARGET}        Target
            ${SHA1}          Dependencies 8-char sha1 prefix
            ${HASH:len}      DAG hash with optional length specifier

            ${DEP:name:OPTION} Evaluates as OPTION would for self['name']

            ${SPACK_ROOT}    The spack root directory
            ${SPACK_INSTALL} The default spack install directory,
                             ${SPACK_PREFIX}/opt
            ${PREFIX}        The package prefix
            ${NAMESPACE}     The package namespace

        Note these are case-insensitive: for example you can specify either
        ``${PACKAGE}`` or ``${package}``.

        Optionally you can provide a width, e.g. ``$20_`` for a 20-wide name.
        Like printf, you can provide '-' for left justification, e.g.
        ``$-20_`` for a left-justified name.

        Anything else is copied verbatim into the output stream.

        Args:
            format_string (str): string containing the format to be expanded

        Keyword Args:
            color (bool): True if returned string is colored
            transform (dict): maps full-string formats to a callable \
                that accepts a string and returns another one

        Examples:

            The following line:

            .. code-block:: python

                s = spec.format('$_$@$+')

            translates to the name, version, and options of the package, but no
            dependencies, arch, or compiler.

        TODO: allow, e.g., ``$6#`` to customize short hash length
        TODO: allow, e.g., ``$//`` for full hash.
        """

        color = kwargs.get('color', False)

        # Dictionary of transformations for named tokens
        token_transforms = dict(
            (k.upper(), v) for k, v in kwargs.get('transform', {}).items())

        length = len(format_string)
        out = six.StringIO()
        named = escape = compiler = False
        named_str = fmt = ''

        def write(s, c=None):
            f = clr.cescape(s)
            if c is not None:
                f = color_formats[c] + f + '@.'
            clr.cwrite(f, stream=out, color=color)

        iterator = enumerate(format_string)
        for i, c in iterator:
            if escape:
                fmt = '%'
                if c == '-':
                    fmt += c
                    i, c = next(iterator)

                while c in '0123456789':
                    fmt += c
                    i, c = next(iterator)
                fmt += 's'

                if c == '_':
                    name = self.name if self.name else ''
                    out.write(fmt % name)
                elif c == '.':
                    name = self.fullname if self.fullname else ''
                    out.write(fmt % name)
                elif c == '@':
                    if self.versions and self.versions != _any_version:
                        write(fmt % (c + str(self.versions)), c)
                elif c == '%':
                    if self.compiler:
                        write(fmt % (c + str(self.compiler.name)), c)
                    compiler = True
                elif c == '+':
                    if self.variants:
                        write(fmt % str(self.variants), c)
                elif c == '=':
                    if self.architecture and str(self.architecture):
                        a_str = ' arch' + c + str(self.architecture) + ' '
                        write(fmt % (a_str), c)
                elif c == '/':
                    out.write('/' + fmt % (self.dag_hash(7)))
                elif c == '$':
                    if fmt != '%s':
                        raise ValueError("Can't use format width with $$.")
                    out.write('$')
                elif c == '{':
                    named = True
                    named_str = ''
                escape = False

            elif compiler:
                if c == '@':
                    if (self.compiler and self.compiler.versions and
                            self.compiler.versions != _any_version):
                        write(c + str(self.compiler.versions), '%')
                elif c == '+':
                    if self.compiler_flags:
                        write(fmt % str(self.compiler_flags), '%')
                    compiler = False
                elif c == '$':
                    escape = True
                    compiler = False
                else:
                    out.write(c)
                    compiler = False

            elif named:
                if not c == '}':
                    if i == length - 1:
                        raise ValueError("Error: unterminated ${ in format:"
                                         "'%s'" % format_string)
                    named_str += c
                    continue
                named_str = named_str.upper()

                # Retrieve the token transformation from the dictionary.
                #
                # The default behavior is to leave the string unchanged
                # (`lambda x: x` is the identity function)
                transform = token_transforms.get(named_str, lambda s, x: x)

                if named_str == 'PACKAGE':
                    name = self.name if self.name else ''
                    write(fmt % transform(self, name))
                elif named_str == 'FULLPACKAGE':
                    name = self.fullname if self.fullname else ''
                    write(fmt % transform(self, name))
                elif named_str == 'VERSION':
                    if self.versions and self.versions != _any_version:
                        write(fmt % transform(self, str(self.versions)), '@')
                elif named_str == 'COMPILER':
                    if self.compiler:
                        write(fmt % transform(self, self.compiler), '%')
                elif named_str == 'COMPILERNAME':
                    if self.compiler:
                        write(fmt % transform(self, self.compiler.name), '%')
                elif named_str in ['COMPILERVER', 'COMPILERVERSION']:
                    if self.compiler:
                        write(
                            fmt % transform(self, self.compiler.versions),
                            '%'
                        )
                elif named_str == 'COMPILERFLAGS':
                    if self.compiler:
                        write(
                            fmt % transform(self, str(self.compiler_flags)),
                            '%'
                        )
                elif named_str == 'OPTIONS':
                    if self.variants:
                        write(fmt % transform(self, str(self.variants)), '+')
                elif named_str in ["ARCHITECTURE", "PLATFORM", "TARGET", "OS"]:
                    if self.architecture and str(self.architecture):
                        if named_str == "ARCHITECTURE":
                            write(
                                fmt % transform(self, str(self.architecture)),
                                '='
                            )
                        elif named_str == "PLATFORM":
                            platform = str(self.architecture.platform)
                            write(fmt % transform(self, platform), '=')
                        elif named_str == "OS":
                            operating_sys = str(self.architecture.os)
                            write(fmt % transform(self, operating_sys), '=')
                        elif named_str == "TARGET":
                            target = str(self.architecture.target)
                            write(fmt % transform(self, target), '=')
                elif named_str == 'SHA1':
                    if self.dependencies:
                        out.write(fmt % transform(self, str(self.dag_hash(7))))
                elif named_str == 'SPACK_ROOT':
                    out.write(fmt % transform(self, spack.paths.prefix))
                elif named_str == 'SPACK_INSTALL':
                    out.write(fmt % transform(self, spack.store.root))
                elif named_str == 'PREFIX':
                    out.write(fmt % transform(self, self.prefix))
                elif named_str.startswith('HASH'):
                    if named_str.startswith('HASH:'):
                        _, hashlen = named_str.split(':')
                        hashlen = int(hashlen)
                    else:
                        hashlen = None
                    out.write(fmt % (self.dag_hash(hashlen)))
                elif named_str == 'NAMESPACE':
                    out.write(fmt % transform(self, self.namespace))
                elif named_str.startswith('DEP:'):
                    _, dep_name, dep_option = named_str.lower().split(':', 2)
                    dep_spec = self[dep_name]
                    out.write(fmt % (dep_spec.format('${%s}' % dep_option)))

                named = False

            elif c == '$':
                escape = True
                if i == length - 1:
                    raise ValueError("Error: unterminated $ in format: '%s'"
                                     % format_string)
            else:
                out.write(c)

        result = out.getvalue()
        return result

    def cformat(self, *args, **kwargs):
        """Same as format, but color defaults to auto instead of False."""
        kwargs = kwargs.copy()
        kwargs.setdefault('color', None)
        return self.format(*args, **kwargs)

    def dep_string(self):
        return ''.join(" ^" + dep.format() for dep in self.sorted_deps())

    def __str__(self):
        ret = self.format() + self.dep_string()
        return ret.strip()

    def install_status(self):
        """Helper for tree to print DB install status."""
        if not self.concrete:
            return None
        try:
            record = spack.store.db.get_record(self)
            return record.installed
        except KeyError:
            return None

    def _installed_explicitly(self):
        """Helper for tree to print DB install status."""
        if not self.concrete:
            return None
        try:
            record = spack.store.db.get_record(self)
            return record.explicit
        except KeyError:
            return None

    def tree(self, **kwargs):
        """Prints out this spec and its dependencies, tree-formatted
           with indentation."""
        color = kwargs.pop('color', clr.get_color_when())
        depth = kwargs.pop('depth', False)
        hashes = kwargs.pop('hashes', False)
        hlen = kwargs.pop('hashlen', None)
        status_fn = kwargs.pop('status_fn', False)
        cover = kwargs.pop('cover', 'nodes')
        indent = kwargs.pop('indent', 0)
        fmt = kwargs.pop('format', default_format)
        prefix = kwargs.pop('prefix', None)
        show_types = kwargs.pop('show_types', False)
        deptypes = kwargs.pop('deptypes', 'all')
        recurse_dependencies = kwargs.pop('recurse_dependencies', True)
        lang.check_kwargs(kwargs, self.tree)

        out = ""
        for d, dep_spec in self.traverse_edges(
                order='pre', cover=cover, depth=True, deptypes=deptypes):
            node = dep_spec.spec

            if prefix is not None:
                out += prefix(node)
            out += " " * indent

            if depth:
                out += "%-4d" % d

            if status_fn:
                status = status_fn(node)
                if node.package.installed_upstream:
                    out += clr.colorize("@g{[^]}  ", color=color)
                elif status is None:
                    out += clr.colorize("@K{ - }  ", color=color)  # !installed
                elif status:
                    out += clr.colorize("@g{[+]}  ", color=color)  # installed
                else:
                    out += clr.colorize("@r{[-]}  ", color=color)  # missing

            if hashes:
                out += clr.colorize(
                    '@K{%s}  ', color=color) % node.dag_hash(hlen)

            if show_types:
                if cover == 'nodes':
                    # when only covering nodes, we merge dependency types
                    # from all dependents before showing them.
                    types = [
                        ds.deptypes for ds in node.dependents_dict().values()]
                else:
                    # when covering edges or paths, we show dependency
                    # types only for the edge through which we visited
                    types = [dep_spec.deptypes]

                type_chars = dp.deptype_chars(*types)
                out += '[%s]  ' % type_chars

            out += ("    " * d)
            if d > 0:
                out += "^"
            out += node.format(fmt, color=color) + "\n"

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
        Suppose, however, that we wish to use a differently-built H, known as
        H'. This function will splice in the new H' in one of two ways:
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
        assert other.name in self

        # Multiple unique specs with the same name will collide, so the
        # _dependents of these specs should not be trusted.
        # Variants may also be ignored here for now...

        if transitive:
            self_nodes = dict((s.name, s.copy(deps=False))
                              for s in self.traverse(root=True)
                              if s.name not in other)
            other_nodes = dict((s.name, s.copy(deps=False))
                               for s in other.traverse(root=True))
        else:
            # If we're not doing a transitive splice, then we only want the
            # root of other.
            self_nodes = dict((s.name, s.copy(deps=False))
                              for s in self.traverse(root=True)
                              if s.name != other.name)
            other_nodes = {other.name: other.copy(deps=False)}

        nodes = other_nodes.copy()
        nodes.update(self_nodes)

        for name in nodes:
            if name in self_nodes:
                dependencies = self[name]._dependencies
                for dep in dependencies:
                    nodes[name]._add_dependency(nodes[dep],
                                                dependencies[dep].deptypes)
                if any(dep not in self_nodes for dep in dependencies):
                    nodes[name].build_spec = self[name].build_spec
            else:
                dependencies = other[name]._dependencies
                for dep in dependencies:
                    nodes[name]._add_dependency(nodes[dep],
                                                dependencies[dep].deptypes)
                if any(dep not in other_nodes for dep in dependencies):
                    nodes[name].build_spec = other[name].build_spec

        # Clear cached hashes
        nodes[self.name].clear_cached_hashes()
        return nodes[self.name]

    def clear_cached_hashes(self):
        """
        Clears all cached hashes in a Spec, while preserving other properties.
        """
        for attr in ht.SpecHashDescriptor.hash_types:
            if hasattr(self, attr):
                setattr(self, attr, None)


class LazySpecCache(collections.defaultdict):
    """Cache for Specs that uses a spec_like as key, and computes lazily
    the corresponding value ``Spec(spec_like``.
    """
    def __init__(self):
        super(LazySpecCache, self).__init__(Spec)

    def __missing__(self, key):
        value = self.default_factory(key)
        self[key] = value
        return value


#: These are possible token types in the spec grammar.
HASH, DEP, AT, COLON, COMMA, ON, OFF, PCT, EQ, ID, VAL, FILE = range(12)

#: Regex for fully qualified spec names. (e.g., builtin.hdf5)
spec_id_re = r'\w[\w.-]*'


class SpecLexer(spack.parse.Lexer):

    """Parses tokens that make up spack specs."""

    def __init__(self):
        super(SpecLexer, self).__init__([
            (r'\^', lambda scanner, val: self.token(DEP,   val)),
            (r'\@', lambda scanner, val: self.token(AT,    val)),
            (r'\:', lambda scanner, val: self.token(COLON, val)),
            (r'\,', lambda scanner, val: self.token(COMMA, val)),
            (r'\+', lambda scanner, val: self.token(ON,    val)),
            (r'\-', lambda scanner, val: self.token(OFF,   val)),
            (r'\~', lambda scanner, val: self.token(OFF,   val)),
            (r'\%', lambda scanner, val: self.token(PCT,   val)),
            (r'\=', lambda scanner, val: self.token(EQ,    val)),

            # Filenames match before identifiers, so no initial filename
            # component is parsed as a spec (e.g., in subdir/spec.yaml)
            (r'[/\w.-]*/[/\w/-]+\.yaml[^\b]*',
             lambda scanner, v: self.token(FILE, v)),

            # Hash match after filename. No valid filename can be a hash
            # (files end w/.yaml), but a hash can match a filename prefix.
            (r'/', lambda scanner, val: self.token(HASH, val)),

            # Identifiers match after filenames and hashes.
            (spec_id_re, lambda scanner, val: self.token(ID, val)),

            (r'\s+', lambda scanner, val: None)],
            [EQ],
            [(r'[\S].*', lambda scanner, val: self.token(VAL,    val)),
             (r'\s+', lambda scanner, val: None)],
            [VAL])


# Lexer is always the same for every parser.
_lexer = SpecLexer()


class SpecParser(spack.parse.Parser):

    def __init__(self, initial_spec=None):
        """Construct a new SpecParser.

        Args:
            initial_spec (Spec, optional): provide a Spec that we'll parse
                directly into. This is used to avoid construction of a
                superfluous Spec object in the Spec constructor.
        """
        super(SpecParser, self).__init__(_lexer)
        self.previous = None
        self._initial = initial_spec

    def do_parse(self):
        specs = []

        try:
            while self.next:
                # Try a file first, but if it doesn't succeed, keep parsing
                # as from_file may backtrack and try an id.
                if self.accept(FILE):
                    spec = self.spec_from_file()
                    if spec:
                        specs.append(spec)
                        continue

                if self.accept(ID):
                    self.previous = self.token
                    if self.accept(EQ):
                        # We're parsing an anonymous spec beginning with a
                        # key-value pair.
                        if not specs:
                            self.push_tokens([self.previous, self.token])
                            self.previous = None
                            specs.append(self.spec(None))
                        else:
                            if specs[-1].concrete:
                                # Trying to add k-v pair to spec from hash
                                raise RedundantSpecError(specs[-1],
                                                         'key-value pair')
                            # We should never end up here.
                            # This requires starting a new spec with ID, EQ
                            # After another spec that is not concrete
                            # If the previous spec is not concrete, this is
                            # handled in the spec parsing loop
                            # If it is concrete, see the if statement above
                            # If there is no previous spec, we don't land in
                            # this else case.
                            self.unexpected_token()
                    else:
                        # We're parsing a new spec by name
                        self.previous = None
                        specs.append(self.spec(self.token.value))
                elif self.accept(HASH):
                    # We're finding a spec by hash
                    specs.append(self.spec_by_hash())

                elif self.accept(DEP):
                    if not specs:
                        # We're parsing an anonymous spec beginning with a
                        # dependency. Push the token to recover after creating
                        # anonymous spec
                        self.push_tokens([self.token])
                        specs.append(self.spec(None))
                    else:
                        dep = None
                        if self.accept(FILE):
                            # this may return None, in which case we backtrack
                            dep = self.spec_from_file()

                        if not dep and self.accept(HASH):
                            # We're finding a dependency by hash for an
                            # anonymous spec
                            dep = self.spec_by_hash()
                            dep = dep.copy(deps=('link', 'run'))

                        if not dep:
                            # We're adding a dependency to the last spec
                            if self.accept(ID):
                                self.previous = self.token
                                if self.accept(EQ):
                                    # This is an anonymous dep with a key=value
                                    # push tokens to be parsed as part of the
                                    # dep spec
                                    self.push_tokens(
                                        [self.previous, self.token])
                                    dep_name = None
                                else:
                                    # named dep (standard)
                                    dep_name = self.token.value
                                self.previous = None
                            else:
                                # anonymous dep
                                dep_name = None
                            dep = self.spec(dep_name)

                        # Raise an error if the previous spec is already
                        # concrete (assigned by hash)
                        if specs[-1]._hash:
                            raise RedundantSpecError(specs[-1], 'dependency')
                        # command line deps get empty deptypes now.
                        # Real deptypes are assigned later per packages.
                        specs[-1]._add_dependency(dep, ())

                else:
                    # If the next token can be part of a valid anonymous spec,
                    # create the anonymous spec
                    if self.next.type in (AT, ON, OFF, PCT):
                        # Raise an error if the previous spec is already
                        # concrete (assigned by hash)
                        if specs and specs[-1]._hash:
                            raise RedundantSpecError(specs[-1],
                                                     'compiler, version, '
                                                     'or variant')
                        specs.append(self.spec(None))
                    else:
                        self.unexpected_token()

        except spack.parse.ParseError as e:
            raise SpecParseError(e)

        return specs

    def spec_from_file(self):
        """Read a spec from a filename parsed on the input stream.

        There is some care taken here to ensure that filenames are a last
        resort, and that any valid package name is parsed as a name
        before we consider it as a file. Specs are used in lots of places;
        we don't want the parser touching the filesystem unnecessarily.

        The parse logic is as follows:

        1. We require that filenames end in .yaml, which means that no valid
           filename can be interpreted as a hash (hashes can't have '.')

        2. We avoid treating paths like /path/to/spec.yaml as hashes, or paths
           like subdir/spec.yaml as ids by lexing filenames before hashes.

        3. For spec names that match file and id regexes, like 'builtin.yaml',
           we backtrack from spec_from_file() and treat them as spec names.

        """
        path = self.token.value

        # Special case where someone omits a space after a filename. Consider:
        #
        #     libdwarf^/some/path/to/libelf.yamllibdwarf ^../../libelf.yaml
        #
        # The error is clearly an omitted space. To handle this, the FILE
        # regex admits text *beyond* .yaml, and we raise a nice error for
        # file names that don't end in .yaml.
        if not path.endswith(".yaml"):
            raise SpecFilenameError(
                "Spec filename must end in .yaml: '{0}'".format(path))

        if not os.path.exists(path):
            raise NoSuchSpecFileError("No such spec file: '{0}'".format(path))

        with open(path) as f:
            return Spec.from_yaml(f)

    def parse_compiler(self, text):
        self.setup(text)
        return self.compiler()

    def spec_by_hash(self):
        self.expect(ID)

        dag_hash = self.token.value
        matches = spack.store.db.get_by_hash(dag_hash)
        if not matches:
            raise NoSuchHashError(dag_hash)

        if len(matches) != 1:
            raise AmbiguousHashError(
                "Multiple packages specify hash beginning '%s'."
                % dag_hash, *matches)

        return matches[0]

    def spec(self, name):
        """Parse a spec out of the input. If a spec is supplied, initialize
           and return it instead of creating a new one."""
        spec_namespace = None
        spec_name = None
        if name:
            spec_namespace, dot, spec_name = name.rpartition('.')
            if not spec_namespace:
                spec_namespace = None
            self.check_identifier(spec_name)

        if self._initial is None:
            spec = Spec()
        else:
            # this is used by Spec.__init__
            spec = self._initial
            self._initial = None

        spec.namespace = spec_namespace
        spec.name = spec_name

        while self.next:
            if self.accept(AT):
                vlist = self.version_list()
                spec._add_versions(vlist)

            elif self.accept(ON):
                name = self.variant()
                spec.variants[name] = vt.BoolValuedVariant(name, True)

            elif self.accept(OFF):
                name = self.variant()
                spec.variants[name] = vt.BoolValuedVariant(name, False)

            elif self.accept(PCT):
                spec._set_compiler(self.compiler())

            elif self.accept(ID):
                self.previous = self.token
                if self.accept(EQ):
                    # We're adding a key-value pair to the spec
                    self.expect(VAL)
                    spec._add_flag(self.previous.value, self.token.value)
                    self.previous = None
                else:
                    # We've found the start of a new spec. Go back to do_parse
                    # and read this token again.
                    self.push_tokens([self.token])
                    self.previous = None
                    break

            elif self.accept(HASH):
                # Get spec by hash and confirm it matches what we already have
                hash_spec = self.spec_by_hash()
                if hash_spec.satisfies(spec):
                    spec._dup(hash_spec)
                    break
                else:
                    raise InvalidHashError(spec, hash_spec.dag_hash())

            else:
                break

        spec._add_default_platform()
        return spec

    def variant(self, name=None):
        if name:
            return name
        else:
            self.expect(ID)
            self.check_identifier()
            return self.token.value

    def version(self):
        start = None
        end = None
        if self.accept(ID):
            start = self.token.value

        if self.accept(COLON):
            if self.accept(ID):
                if self.next and self.next.type is EQ:
                    # This is a start: range followed by a key=value pair
                    self.push_tokens([self.token])
                else:
                    end = self.token.value
        elif start:
            # No colon, but there was a version.
            return vn.Version(start)
        else:
            # No colon and no id: invalid version.
            self.next_token_error("Invalid version specifier")

        if start:
            start = vn.Version(start)
        if end:
            end = vn.Version(end)
        return vn.VersionRange(start, end)

    def version_list(self):
        vlist = []
        vlist.append(self.version())
        while self.accept(COMMA):
            vlist.append(self.version())
        return vlist

    def compiler(self):
        self.expect(ID)
        self.check_identifier()

        compiler = CompilerSpec.__new__(CompilerSpec)
        compiler.name = self.token.value
        compiler.versions = vn.VersionList()
        if self.accept(AT):
            vlist = self.version_list()
            compiler._add_versions(vlist)
        else:
            compiler.versions = vn.VersionList(':')
        return compiler

    def check_identifier(self, id=None):
        """The only identifiers that can contain '.' are versions, but version
           ids are context-sensitive so we have to check on a case-by-case
           basis. Call this if we detect a version id where it shouldn't be.
        """
        if not id:
            id = self.token.value
        if '.' in id:
            self.last_token_error(
                "{0}: Identifier cannot contain '.'".format(id))


def parse(string):
    """Returns a list of specs from an input string.
       For creating one spec, see Spec() constructor.
    """
    return SpecParser().parse(string)


def save_dependency_spec_yamls(
        root_spec_as_yaml, output_directory, dependencies=None):
    """Given a root spec (represented as a yaml object), index it with a subset
       of its dependencies, and write each dependency to a separate yaml file
       in the output directory.  By default, all dependencies will be written
       out.  To choose a smaller subset of dependencies to be written, pass a
       list of package names in the dependencies parameter.  In case of any
       kind of error, SaveSpecDependenciesError is raised with a specific
       message about what went wrong."""
    root_spec = Spec.from_yaml(root_spec_as_yaml)

    dep_list = dependencies
    if not dep_list:
        dep_list = [dep.name for dep in root_spec.traverse()]

    for dep_name in dep_list:
        if dep_name not in root_spec:
            msg = 'Dependency {0} does not exist in root spec {1}'.format(
                dep_name, root_spec.name)
            raise SpecDependencyNotFoundError(msg)
        dep_spec = root_spec[dep_name]
        yaml_path = os.path.join(output_directory, '{0}.yaml'.format(dep_name))

        with open(yaml_path, 'w') as fd:
            fd.write(dep_spec.to_yaml(hash=ht.build_hash))


def base32_prefix_bits(hash_string, bits):
    """Return the first <bits> bits of a base32 string as an integer."""
    if bits > len(hash_string) * 5:
        raise ValueError("Too many bits! Requested %d bit prefix of '%s'."
                         % (bits, hash_string))

    hash_bytes = base64.b32decode(hash_string, casefold=True)
    return spack.util.crypto.prefix_bits(hash_bytes, bits)


class SpecParseError(spack.error.SpecError):
    """Wrapper for ParseError for when we're parsing specs."""
    def __init__(self, parse_error):
        super(SpecParseError, self).__init__(parse_error.message)
        self.string = parse_error.string
        self.pos = parse_error.pos


class DuplicateDependencyError(spack.error.SpecError):
    """Raised when the same dependency occurs in a spec twice."""


class MultipleVersionError(spack.error.SpecError):
    """Raised when version constraints occur in a spec twice."""


class DuplicateCompilerSpecError(spack.error.SpecError):
    """Raised when the same compiler occurs in a spec twice."""


class UnsupportedCompilerError(spack.error.SpecError):
    """Raised when the user asks for a compiler spack doesn't know about."""
    def __init__(self, compiler_name):
        super(UnsupportedCompilerError, self).__init__(
            "The '%s' compiler is not yet supported." % compiler_name)


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
        super(InvalidDependencyError, self).__init__(
            'Package {0} does not depend on {1}'.format(
                pkg, spack.util.string.comma_or(deps)))


class NoProviderError(spack.error.SpecError):
    """Raised when there is no package that provides a particular
       virtual dependency.
    """
    def __init__(self, vpkg):
        super(NoProviderError, self).__init__(
            "No providers found for virtual package: '%s'" % vpkg)
        self.vpkg = vpkg


class MultipleProviderError(spack.error.SpecError):
    """Raised when there is no package that provides a particular
       virtual dependency.
    """
    def __init__(self, vpkg, providers):
        """Takes the name of the vpkg"""
        super(MultipleProviderError, self).__init__(
            "Multiple providers found for '%s': %s"
            % (vpkg, [str(s) for s in providers]))
        self.vpkg = vpkg
        self.providers = providers


class UnsatisfiableSpecNameError(spack.error.UnsatisfiableSpecError):
    """Raised when two specs aren't even for the same package."""
    def __init__(self, provided, required):
        super(UnsatisfiableSpecNameError, self).__init__(
            provided, required, "name")


class UnsatisfiableVersionSpecError(spack.error.UnsatisfiableSpecError):
    """Raised when a spec version conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableVersionSpecError, self).__init__(
            provided, required, "version")


class UnsatisfiableCompilerSpecError(spack.error.UnsatisfiableSpecError):
    """Raised when a spec comiler conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableCompilerSpecError, self).__init__(
            provided, required, "compiler")


class UnsatisfiableCompilerFlagSpecError(spack.error.UnsatisfiableSpecError):
    """Raised when a spec variant conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableCompilerFlagSpecError, self).__init__(
            provided, required, "compiler_flags")


class UnsatisfiableArchitectureSpecError(spack.error.UnsatisfiableSpecError):
    """Raised when a spec architecture conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableArchitectureSpecError, self).__init__(
            provided, required, "architecture")


class UnsatisfiableProviderSpecError(spack.error.UnsatisfiableSpecError):
    """Raised when a provider is supplied but constraints don't match
       a vpkg requirement"""
    def __init__(self, provided, required):
        super(UnsatisfiableProviderSpecError, self).__init__(
            provided, required, "provider")


# TODO: get rid of this and be more specific about particular incompatible
# dep constraints
class UnsatisfiableDependencySpecError(spack.error.UnsatisfiableSpecError):
    """Raised when some dependency of constrained specs are incompatible"""
    def __init__(self, provided, required):
        super(UnsatisfiableDependencySpecError, self).__init__(
            provided, required, "dependency")


class UnconstrainableDependencySpecError(spack.error.SpecError):
    """Raised when attempting to constrain by an anonymous dependency spec"""
    def __init__(self, spec):
        msg = "Cannot constrain by spec '%s'. Cannot constrain by a" % spec
        msg += " spec containing anonymous dependencies"
        super(UnconstrainableDependencySpecError, self).__init__(msg)


class AmbiguousHashError(spack.error.SpecError):
    def __init__(self, msg, *specs):
        spec_fmt = '{namespace}.{name}{@version}{%compiler}{compiler_flags}'
        spec_fmt += '{variants}{arch=architecture}{/hash:7}'
        specs_str = '\n  ' + '\n  '.join(spec.format(spec_fmt)
                                         for spec in specs)
        super(AmbiguousHashError, self).__init__(msg + specs_str)


class InvalidHashError(spack.error.SpecError):
    def __init__(self, spec, hash):
        super(InvalidHashError, self).__init__(
            "The spec specified by %s does not match provided spec %s"
            % (hash, spec))


class NoSuchHashError(spack.error.SpecError):
    def __init__(self, hash):
        super(NoSuchHashError, self).__init__(
            "No installed spec matches the hash: '%s'"
            % hash)


class SpecFilenameError(spack.error.SpecError):
    """Raised when a spec file name is invalid."""


class NoSuchSpecFileError(SpecFilenameError):
    """Raised when a spec file doesn't exist."""


class RedundantSpecError(spack.error.SpecError):
    def __init__(self, spec, addition):
        super(RedundantSpecError, self).__init__(
            "Attempting to add %s to spec %s which is already concrete."
            " This is likely the result of adding to a spec specified by hash."
            % (addition, spec))


class SpecFormatStringError(spack.error.SpecError):
    """Called for errors in Spec format strings."""


class SpecFormatSigilError(SpecFormatStringError):
    """Called for mismatched sigils and attributes in format strings"""
    def __init__(self, sigil, requirement, used):
        msg = 'The sigil %s may only be used for %s.' % (sigil, requirement)
        msg += ' It was used with the attribute %s.' % used
        super(SpecFormatSigilError, self).__init__(msg)


class ConflictsInSpecError(spack.error.SpecError, RuntimeError):
    def __init__(self, spec, matches):
        message = 'Conflicts in concretized spec "{0}"\n'.format(
            spec.short_spec
        )

        visited = set()

        long_message = ''

        match_fmt_default = '{0}. "{1}" conflicts with "{2}"\n'
        match_fmt_custom = '{0}. "{1}" conflicts with "{2}" [{3}]\n'

        for idx, (s, c, w, msg) in enumerate(matches):

            if s not in visited:
                visited.add(s)
                long_message += 'List of matching conflicts for spec:\n\n'
                long_message += s.tree(indent=4) + '\n'

            if msg is None:
                long_message += match_fmt_default.format(idx + 1, c, w)
            else:
                long_message += match_fmt_custom.format(idx + 1, c, w, msg)

        super(ConflictsInSpecError, self).__init__(message, long_message)


class SpecDependencyNotFoundError(spack.error.SpecError):
    """Raised when a failure is encountered writing the dependencies of
    a spec."""


class SpecDeprecatedError(spack.error.SpecError):
    """Raised when a spec concretizes to a deprecated spec or dependency."""


class InvalidSpecDetected(spack.error.SpecError):
    """Raised when a detected spec doesn't pass validation checks."""
