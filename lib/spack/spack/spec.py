##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""
Spack allows very fine-grained control over how packages are installed and
over how they are built and configured.  To make this easy, it has its own
syntax for declaring a dependence.  We call a descriptor of a particular
package configuration a "spec".

The syntax looks like this:

.. code-block:: sh

    $ spack install mpileaks ^openmpi @1.2:1.4 +debug %intel @12.1 =bgqos_0
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
import ctypes
import hashlib
import itertools
import os

from operator import attrgetter
from six import StringIO
from six import string_types
from six import iteritems

from llnl.util.filesystem import find_headers, find_libraries, is_exe
from llnl.util.lang import *
from llnl.util.tty.color import *

import spack
import spack.architecture
import spack.compilers as compilers
import spack.error
import spack.parse
import spack.store
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml

from spack.util.module_cmd import get_path_from_module, load_module
from spack.error import SpecError, UnsatisfiableSpecError
from spack.provider_index import ProviderIndex
from spack.util.crypto import prefix_bits
from spack.util.executable import Executable
from spack.util.prefix import Prefix
from spack.util.spack_yaml import syaml_dict
from spack.util.string import *
from spack.variant import *
from spack.version import *
from yaml.error import MarkedYAMLError

__all__ = [
    'Spec',
    'alldeps',
    'canonical_deptype',
    'parse',
    'parse_anonymous_spec',
    'SpecError',
    'SpecParseError',
    'DuplicateDependencyError',
    'DuplicateVariantError',
    'DuplicateCompilerSpecError',
    'UnsupportedCompilerError',
    'UnknownVariantError',
    'DuplicateArchitectureError',
    'InconsistentSpecError',
    'InvalidDependencyError',
    'NoProviderError',
    'MultipleProviderError',
    'UnsatisfiableSpecError',
    'UnsatisfiableSpecNameError',
    'UnsatisfiableVersionSpecError',
    'UnsatisfiableCompilerSpecError',
    'UnsatisfiableVariantSpecError',
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
#: See spack.color for descriptions of the color codes.
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
_any_version = VersionList([':'])

#: Types of dependencies that Spack understands.
alldeps = ('build', 'link', 'run')

#: Max integer helps avoid passing too large a value to cyaml.
maxint = 2 ** (ctypes.sizeof(ctypes.c_int) * 8 - 1) - 1


def canonical_deptype(deptype):
    if deptype in (None, 'all', all):
        return alldeps

    elif isinstance(deptype, string_types):
        if deptype not in alldeps:
            raise ValueError('Invalid dependency type: %s' % deptype)
        return (deptype,)

    elif isinstance(deptype, (tuple, list)):
        invalid = next((d for d in deptype if d not in alldeps), None)
        if invalid:
            raise ValueError('Invalid dependency type: %s' % invalid)
        return tuple(sorted(deptype))

    return deptype


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
                return cescape(sep)
            self.last = sep

            return '%s%s' % (color_formats[sep], cescape(sep))

    return colorize(re.sub(_separators, insert_color(), str(spec)) + '@.')


@key_ordering
class ArchSpec(object):
    """ The ArchSpec class represents an abstract architecture specification
        that a package should be built with.  At its core, each ArchSpec is
        comprised of three elements: a platform (e.g. Linux), an OS (e.g.
        RHEL6), and a target (e.g. x86_64).
    """

    # TODO: Formalize the specifications for architectures and then use
    # the appropriate parser here to read these specifications.
    def __init__(self, *args):
        to_attr_string = lambda s: str(s) if s and s != "None" else None

        self.platform, self.platform_os, self.target = (None, None, None)

        if len(args) == 1:
            spec_like = args[0]
            if isinstance(spec_like, ArchSpec):
                self._dup(spec_like)
            elif isinstance(spec_like, string_types):
                spec_fields = spec_like.split("-")

                if len(spec_fields) == 3:
                    self.platform, self.platform_os, self.target = tuple(
                        to_attr_string(f) for f in spec_fields)
                else:
                    raise ValueError("%s is an invalid arch spec" % spec_like)
        elif len(args) == 3:
            self.platform = to_attr_string(args[0])
            self.platform_os = to_attr_string(args[1])
            self.target = to_attr_string(args[2])
        elif len(args) != 0:
            raise TypeError("Can't make arch spec from %s" % args)

    def _autospec(self, spec_like):
        if isinstance(spec_like, ArchSpec):
            return spec_like
        return ArchSpec(spec_like)

    def _cmp_key(self):
        return (self.platform, self.platform_os, self.target)

    def _dup(self, other):
        self.platform = other.platform
        self.platform_os = other.platform_os
        self.target = other.target

    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, value):
        """ The platform of the architecture spec will be verified as a
            supported Spack platform before it's set to ensure all specs
            refer to valid platforms.
        """
        value = str(value) if value is not None else None
        self._platform = value

    @property
    def platform_os(self):
        return self._platform_os

    @platform_os.setter
    def platform_os(self, value):
        """ The OS of the architecture spec will update the platform field
            if the OS is set to one of the reserved OS types so that the
            default OS type can be resolved.  Since the reserved OS
            information is only available for the host machine, the platform
            will assumed to be the host machine's platform.
        """
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

        self._platform_os = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        """ The target of the architecture spec will update the platform field
            if the target is set to one of the reserved target types so that
            the default target type can be resolved.  Since the reserved target
            information is only available for the host machine, the platform
            will assumed to be the host machine's platform.
        """
        value = str(value) if value is not None else None

        if value in spack.architecture.Platform.reserved_targets:
            curr_platform = str(spack.architecture.platform())
            self.platform = self.platform or curr_platform

            if self.platform != curr_platform:
                raise ValueError(
                    "Can't set arch spec target to reserved value '%s' when "
                    "the arch platform (%s) isn't the current platform (%s)" %
                    (value, self.platform, curr_platform))

            spec_platform = spack.architecture.get_platform(self.platform)
            value = str(spec_platform.target(value))

        self._target = value

    def satisfies(self, other, strict=False):
        other = self._autospec(other)
        sdict, odict = self.to_cmp_dict(), other.to_cmp_dict()

        if strict or self.concrete:
            return all(getattr(self, attr) == getattr(other, attr)
                       for attr in odict if odict[attr])
        else:
            return all(getattr(self, attr) == getattr(other, attr)
                       for attr in odict if sdict[attr] and odict[attr])

    def constrain(self, other):
        """ Projects all architecture fields that are specified in the given
            spec onto the instance spec if they're missing from the instance
            spec. This will only work if the two specs are compatible.
        """
        other = self._autospec(other)

        if not self.satisfies(other):
            raise UnsatisfiableArchitectureSpecError(self, other)

        constrained = False
        for attr, svalue in iteritems(self.to_cmp_dict()):
            ovalue = getattr(other, attr)
            if svalue is None and ovalue is not None:
                setattr(self, attr, ovalue)
                constrained = True

        return constrained

    def copy(self):
        clone = ArchSpec.__new__(ArchSpec)
        clone._dup(self)
        return clone

    @property
    def concrete(self):
        return all(v for k, v in iteritems(self.to_cmp_dict()))

    def to_cmp_dict(self):
        """Returns a dictionary that can be used for field comparison."""
        return dict([
            ('platform', self.platform),
            ('platform_os', self.platform_os),
            ('target', self.target)])

    def to_dict(self):
        d = syaml_dict([
            ('platform', self.platform),
            ('platform_os', self.platform_os),
            ('target', self.target)])
        return syaml_dict([('arch', d)])

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
            return ArchSpec('spack09', 'unknown', d['arch'])

        d = d['arch']
        return ArchSpec(d['platform'], d['platform_os'], d['target'])

    def __str__(self):
        return "%s-%s-%s" % (self.platform, self.platform_os, self.target)

    def __repr__(self):
        return str(self)

    def __contains__(self, string):
        return string in str(self)


@key_ordering
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
            if isinstance(arg, string_types):
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
            self.versions = VersionList()
            self.versions.add(ver(version))

        else:
            raise TypeError(
                "__init__ takes 1 or 2 arguments. (%d given)" % nargs)

    def _add_version(self, version):
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
            raise SpecError("Spec is not concrete: " + str(self))
        return self.versions[0]

    def copy(self):
        clone = CompilerSpec.__new__(CompilerSpec)
        clone.name = self.name
        clone.versions = self.versions.copy()
        return clone

    def _cmp_key(self):
        return (self.name, self.versions)

    def to_dict(self):
        d = syaml_dict([('name', self.name)])
        d.update(self.versions.to_dict())

        return syaml_dict([('compiler', d)])

    @staticmethod
    def from_dict(d):
        d = d['compiler']
        return CompilerSpec(d['name'], VersionList.from_dict(d))

    def __str__(self):
        out = self.name
        if self.versions and self.versions != _any_version:
            vlist = ",".join(str(v) for v in self.versions)
            out += "@%s" % vlist
        return out

    def __repr__(self):
        return str(self)


@key_ordering
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


class FlagMap(HashableMap):

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

    @property
    def concrete(self):
        return all(flag in self for flag in _valid_compiler_flags)

    def copy(self):
        clone = FlagMap(None)
        for name, value in self.items():
            clone[name] = value
        return clone

    def _cmp_key(self):
        return tuple((k, tuple(v)) for k, v in sorted(iteritems(self)))

    def __str__(self):
        sorted_keys = [k for k in sorted(self.keys()) if self[k] != []]
        cond_symbol = ' ' if len(sorted_keys) > 0 else ''
        return cond_symbol + ' '.join(
            str(key) + '=\"' + ' '.join(
                str(f) for f in self[key]) + '\"'
            for key in sorted_keys) + cond_symbol


class DependencyMap(HashableMap):
    """Each spec has a DependencyMap containing specs for its dependencies.
       The DependencyMap is keyed by name. """

    def __init__(self, owner):
        super(DependencyMap, self).__init__()

        # Owner Spec for the current map
        self.owner = owner

    @property
    def concrete(self):

        # Check if the dependencies are concrete and of the correct type
        dependencies_are_concrete = all(
            (d.spec.concrete and d.deptypes) for d in self.values()
        )

        if not dependencies_are_concrete:
            return False

        # If we are dealing with an external spec, it clearly has no
        # dependencies managed by spack
        if self.owner.external:
            return True

        # Now check we have every dependency we need
        pkg = self.owner.package
        for dependency in pkg.dependencies.values():
            # Check that for every condition we satisfy we satisfy also
            # the associated constraint
            for condition, constraint in dependency.items():
                # WARNING: This part relies on the fact that dependencies are
                # the last item to be checked when computing if a spec is
                # concrete. This means that we are ensured that all variants,
                # versions, compilers, etc. are there with their final value
                # when we call 'Spec.satisfies(..., strict=True)'

                # FIXME: at the moment check only for non conditional
                # FIXME: dependencies, to avoid infinite recursion

                # satisfy_condition = self.owner.satisfies(
                #     condition, strict=True
                # )

                satisfy_condition = str(condition) == self.owner.name

                if not satisfy_condition:
                    continue

                dependency_name = constraint.name

                # We don't want to check build dependencies
                if pkg.dependency_types[dependency_name] == set(['build']):
                    continue

                try:
                    dependency = self.owner[dependency_name]
                    satisfy_constraint = dependency.satisfies(
                        constraint, strict=True
                    )
                except KeyError:
                    # If the dependency is not there we don't
                    # satisfy the constraint
                    satisfy_constraint = False

                if satisfy_condition and not satisfy_constraint:
                    return False

        return True

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

    if is_exe(path):
        return Executable(path)
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
        RuntimeError: If no headers are found
    """
    headers = find_headers('*', root=spec.prefix.include, recurse=True)

    if headers:
        return headers
    else:
        msg = 'Unable to locate {0} headers in {1}'
        raise RuntimeError(msg.format(spec.name, spec.prefix.include))


def _libs_default_handler(descriptor, spec, cls):
    """Default handler when looking for the 'libs' attribute.

    Tries to search for ``lib{spec.name}`` recursively starting from
    ``spec.prefix``.

    Parameters:
        descriptor (ForwardQueryToPackage): descriptor that triggered the call
        spec (Spec): spec that is being queried
        cls (type(spec)): type of spec, to match the signature of the
            descriptor ``__get__`` method

    Returns:
        LibraryList: The libraries found

    Raises:
        RuntimeError: If no libraries are found
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
    name = 'lib' + spec.name.replace('-', '?')

    if '+shared' in spec:
        libs = find_libraries(
            name, root=spec.prefix, shared=True, recurse=True
        )
    elif '~shared' in spec:
        libs = find_libraries(
            name, root=spec.prefix, shared=False, recurse=True
        )
    else:
        # Prefer shared
        libs = find_libraries(
            name, root=spec.prefix, shared=True, recurse=True
        )
        if libs:
            return libs

        libs = find_libraries(
            name, root=spec.prefix, shared=False, recurse=True
        )

    if libs:
        return libs
    else:
        msg = 'Unable to recursively locate {0} libraries in {1}'
        raise RuntimeError(msg.format(spec.name, spec.prefix))


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
        # Turn the default handler into a function with the right
        # signature that always returns None
        if default_handler is None:
            default_handler = lambda descriptor, spec, cls: None
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

        If no call can handle the request or a None value is produced,
        then AttributeError is raised.
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
        callbacks_chain.append(lambda: self.default(self, instance, cls))

        # Trigger the callbacks in order, the first one producing a
        # value wins
        value = None
        for f in callbacks_chain:
            try:
                value = f()
                break
            except AttributeError:
                pass
        # 'None' value raises AttributeError : this permits to 'disable'
        # the call in a particular package by returning None from the
        # queried attribute, or will trigger an exception if  things
        # searched for were not found
        if value is None:
            fmt = '\'{name}\' package has no relevant attribute \'{query}\'\n'  # NOQA: ignore=E501
            fmt += '\tspec : \'{spec}\'\n'
            fmt += '\tqueried as : \'{spec.last_query.name}\'\n'
            fmt += '\textra parameters : \'{spec.last_query.extra_parameters}\'\n'  # NOQA: ignore=E501
            message = fmt.format(
                name=pkg.name,
                query=self.attribute_name,
                spec=instance
            )
            raise AttributeError(message)

        return value

    def __set__(self, instance, value):
        cls_name = type(instance).__name__
        msg = "'{0}' object attribute '{1}' is read-only"
        raise AttributeError(msg.format(cls_name, self.attribute_name))


class SpecBuildInterface(ObjectWrapper):
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

        # Represents a query state in a BuildInterface object
        QueryState = collections.namedtuple(
            'QueryState', ['name', 'extra_parameters', 'isvirtual']
        )

        is_virtual = Spec.is_virtual(name)
        self.last_query = QueryState(
            name=name,
            extra_parameters=query_parameters,
            isvirtual=is_virtual
        )


@key_ordering
class Spec(object):

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

                if isinstance(s, string_types):
                    dag_node, dependency_types = name_and_dependency_types(s)
                else:
                    dag_node, dependency_types = spec_and_dependency_types(s)

                dependency_spec = spec_builder({dag_node: s_dependencies})
                spec._add_dependency(dependency_spec, dependency_types)

            return spec

        return spec_builder(spec_dict)

    def __init__(self, spec_like, **kwargs):
        # Copy if spec_like is a Spec.
        if isinstance(spec_like, Spec):
            self._dup(spec_like)
            return

        # Parse if the spec_like is a string.
        if not isinstance(spec_like, string_types):
            raise TypeError("Can't make spec out of %s" % type(spec_like))

        # parse string types *into* this spec
        spec_list = SpecParser(self).parse(spec_like)
        if len(spec_list) > 1:
            raise ValueError("More than one spec in string: " + spec_like)
        if len(spec_list) < 1:
            raise ValueError("String contains no specs: " + spec_like)

        # Specs are by default not assumed to be normal, but in some
        # cases we've read them from a file want to assume normal.
        # This allows us to manipulate specs that Spack doesn't have
        # package.py files for.
        self._normal = kwargs.get('normal', False)
        self._concrete = kwargs.get('concrete', False)

        # Allow a spec to be constructed with an external path.
        self.external_path = kwargs.get('external_path', None)
        self.external_module = kwargs.get('external_module', None)

    @property
    def external(self):
        return bool(self.external_path) or bool(self.external_module)

    def get_dependency(self, name):
        dep = self._dependencies.get(name)
        if dep is not None:
            return dep
        raise InvalidDependencyError(
            self.name + " does not depend on " + comma_or(name))

    def _find_deps(self, where, deptype):
        deptype = canonical_deptype(deptype)

        return [dep for dep in where.values()
                if deptype and (not dep.deptypes or
                                any(d in deptype for d in dep.deptypes))]

    def dependencies(self, deptype=None):
        return [d.spec
                for d in self._find_deps(self._dependencies, deptype)]

    def dependents(self, deptype=None):
        return [d.parent
                for d in self._find_deps(self._dependents, deptype)]

    def dependencies_dict(self, deptype=None):
        return dict((d.spec.name, d)
                    for d in self._find_deps(self._dependencies, deptype))

    def dependents_dict(self, deptype=None):
        return dict((d.parent.name, d)
                    for d in self._find_deps(self._dependents, deptype))

    #
    # Private routines here are called by the parser when building a spec.
    #
    def _add_version(self, version):
        """Called by the parser to add an allowable version."""
        self.versions.add(version)

    def _add_flag(self, name, value):
        """Called by the parser to add a known flag.
        Known flags currently include "arch"
        """
        valid_flags = FlagMap.valid_compiler_flags()
        if name == 'arch' or name == 'architecture':
            parts = tuple(value.split('-'))
            plat, os, tgt = parts if len(parts) == 3 else (None, None, value)
            self._set_architecture(platform=plat, platform_os=os, target=tgt)
        elif name == 'platform':
            self._set_architecture(platform=value)
        elif name == 'os' or name == 'operating_system':
            self._set_architecture(platform_os=value)
        elif name == 'target':
            self._set_architecture(target=value)
        elif name in valid_flags:
            assert(self.compiler_flags is not None)
            self.compiler_flags[name] = value.split()
        else:
            # FIXME:
            # All other flags represent variants. 'foo=true' and 'foo=false'
            # map to '+foo' and '~foo' respectively. As such they need a
            # BoolValuedVariant instance.
            if str(value).upper() == 'TRUE' or str(value).upper() == 'FALSE':
                self.variants[name] = BoolValuedVariant(name, value)
            else:
                self.variants[name] = AbstractVariant(name, value)

    def _set_architecture(self, **kwargs):
        """Called by the parser to set the architecture."""
        arch_attrs = ['platform', 'platform_os', 'target']
        if self.architecture and self.architecture.concrete:
            raise DuplicateArchitectureError(
                "Spec for '%s' cannot have two architectures." % self.name)

        if not self.architecture:
            new_vals = tuple(kwargs.get(arg, None) for arg in arch_attrs)
            self.architecture = ArchSpec(*new_vals)
        else:
            new_attrvals = [(a, v) for a, v in iteritems(kwargs)
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
           In spack specs, there should be a single root (the package being
           installed).  This will throw an assertion error if that is not
           the case.
        """
        if not self._dependents:
            return self

        # If the spec has multiple dependents, ensure that they all
        # lead to the same place.  Spack shouldn't deal with any DAGs
        # with multiple roots, so something's wrong if we find one.
        depiter = iter(self._dependents.values())
        first_root = next(depiter).parent.root
        assert(all(first_root is d.parent.root for d in depiter))
        return first_root

    @property
    def package(self):
        return spack.repo.get(self)

    @property
    def package_class(self):
        """Internal package call gets only the class object for a package.
           Use this to just get package metadata.
        """
        return spack.repo.get_pkg_class(self.fullname)

    @property
    def virtual(self):
        """Right now, a spec is virtual if no package exists with its name.

           TODO: revisit this -- might need to use a separate namespace and
           be more explicit about this.
           Possible idea: just use conventin and make virtual deps all
           caps, e.g., MPI vs mpi.
        """
        return Spec.is_virtual(self.name)

    @staticmethod
    def is_virtual(name):
        """Test if a name is virtual without requiring a Spec."""
        return (name is not None) and (not spack.repo.exists(name))

    @property
    def concrete(self):
        """A spec is concrete if it can describe only ONE build of a package.
           If any of the name, version, architecture, compiler,
           variants, or depdenencies are ambiguous,then it is not concrete.
        """
        # If we have cached that the spec is concrete, then it's concrete
        if self._concrete:
            return True

        # Otherwise check if the various parts of the spec are concrete.
        # It's crucial to have the check on dependencies last, as it relies
        # on all the other parts to be already checked for concreteness.
        self._concrete = bool(not self.virtual and
                              self.namespace is not None and
                              self.versions.concrete and
                              self.variants.concrete and
                              self.architecture and
                              self.architecture.concrete and
                              self.compiler and self.compiler.concrete and
                              self.compiler_flags.concrete and
                              self._dependencies.concrete)
        return self._concrete

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

    def traverse_edges(self, visited=None, d=0, deptype=None,
                       deptype_query=None, dep_spec=None, **kwargs):
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
        if isinstance(key_fun, string_types):
            key_fun = attrgetter(key_fun)
        yield_root = kwargs.get('root', True)
        cover = kwargs.get('cover', 'nodes')
        direction = kwargs.get('direction', 'children')
        order = kwargs.get('order', 'pre')

        deptype = canonical_deptype(deptype)
        if deptype_query is None:
            deptype_query = ('link', 'run')

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
            # This code determines direction and yields the children/parents
            if direction == 'children':
                successors = self.dependencies_dict(deptype)
                succ = lambda s: s.spec
            elif direction == 'parents':
                successors = self.dependents_dict(deptype)
                succ = lambda s: s.parent
            else:
                raise ValueError('Invalid traversal direction: %s' % direction)

            visited.add(key)
            for name, dspec in sorted(successors.items()):
                child = successors[name]
                children = succ(child).traverse_edges(
                    visited,
                    d=(d + 1),
                    deptype=deptype,
                    deptype_query=deptype_query,
                    dep_spec=dspec,
                    **kwargs)
                for elt in children:
                    yield elt

        # Postorder traversal yields after successors
        if yield_me and order == 'post':
            yield return_val(dep_spec)

    @property
    def short_spec(self):
        """Returns a version of the spec with the dependencies hashed
           instead of completely enumerated."""
        return self.format('$_$@$%@$+$=$/')

    @property
    def cshort_spec(self):
        """Returns an auto-colorized version of ``self.short_spec``."""
        return self.cformat('$_$@$%@$+$=$/')

    @property
    def prefix(self):
        return Prefix(spack.store.layout.path_for_spec(self))

    def dag_hash(self, length=None):
        """Return a hash of the entire spec DAG, including connectivity."""
        if self._hash:
            return self._hash[:length]
        else:
            yaml_text = syaml.dump(
                self.to_node_dict(), default_flow_style=True, width=maxint)
            sha = hashlib.sha1(yaml_text.encode('utf-8'))

            b32_hash = base64.b32encode(sha.digest()).lower()
            if sys.version_info[0] >= 3:
                b32_hash = b32_hash.decode('utf-8')

            if self.concrete:
                self._hash = b32_hash
            return b32_hash[:length]

    def dag_hash_bit_prefix(self, bits):
        """Get the first <bits> bits of the DAG hash as an integer type."""
        return base32_prefix_bits(self.dag_hash(), bits)

    def to_node_dict(self):
        d = syaml_dict()

        if self.versions:
            d.update(self.versions.to_dict())

        if self.architecture:
            d.update(self.architecture.to_dict())

        if self.compiler:
            d.update(self.compiler.to_dict())

        if self.namespace:
            d['namespace'] = self.namespace

        params = syaml_dict(
            sorted(
                v.yaml_entry() for _, v in self.variants.items()
            )
        )
        params.update(sorted(self.compiler_flags.items()))
        if params:
            d['parameters'] = params

        if self.external:
            d['external'] = {
                'path': self.external_path,
                'module': bool(self.external_module)
            }

        # TODO: restore build dependencies here once we have less picky
        # TODO: concretization.
        deps = self.dependencies_dict(deptype=('link', 'run'))
        if deps:
            d['dependencies'] = syaml_dict([
                (name,
                 syaml_dict([
                     ('hash', dspec.spec.dag_hash()),
                     ('type', sorted(str(s) for s in dspec.deptypes))])
                 ) for name, dspec in sorted(deps.items())
            ])

        return syaml_dict([(self.name, d)])

    def to_dict(self):
        node_list = []
        for s in self.traverse(order='pre', deptype=('link', 'run')):
            node = s.to_node_dict()
            node[s.name]['hash'] = s.dag_hash()
            node_list.append(node)

        return syaml_dict([('spec', node_list)])

    def to_yaml(self, stream=None):
        return syaml.dump(
            self.to_dict(), stream=stream, default_flow_style=False)

    def to_json(self, stream=None):
        return sjson.dump(self.to_dict(), stream)

    @staticmethod
    def from_node_dict(node):
        name = next(iter(node))
        node = node[name]

        spec = Spec(name)
        spec.namespace = node.get('namespace', None)
        spec._hash = node.get('hash', None)

        if 'version' in node or 'versions' in node:
            spec.versions = VersionList.from_dict(node)

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
                    spec.variants[name] = MultiValuedVariant.from_node_dict(
                        name, value
                    )
        elif 'variants' in node:
            for name, value in node['variants'].items():
                spec.variants[name] = MultiValuedVariant.from_node_dict(
                    name, value
                )
            for name in FlagMap.valid_compiler_flags():
                spec.compiler_flags[name] = []

        if 'external' in node:
            spec.external_path = None
            spec.external_module = None
            # This conditional is needed because sometimes this function is
            # called with a node already constructed that contains a 'versions'
            # and 'external' field. Related to virtual packages provider
            # indexes.
            if node['external']:
                spec.external_path = node['external']['path']
                spec.external_module = node['external']['module']
                if spec.external_module is False:
                    spec.external_module = None
        else:
            spec.external_path = None
            spec.external_module = None

        # Don't read dependencies here; from_node_dict() is used by
        # from_yaml() to read the root *and* each dependency spec.

        return spec

    @staticmethod
    def read_yaml_dep_specs(dependency_dict):
        """Read the DependencySpec portion of a YAML-formatted Spec.

        This needs to be backward-compatible with older spack spec
        formats so that reindex will work on old specs/databases.
        """
        for dep_name, elt in dependency_dict.items():
            if isinstance(elt, string_types):
                # original format, elt is just the dependency hash.
                dag_hash, deptypes = elt, ['build', 'link']
            elif isinstance(elt, tuple):
                # original deptypes format: (used tuples, not future-proof)
                dag_hash, deptypes = elt
            elif isinstance(elt, dict):
                # new format: elements of dependency spec are keyed.
                dag_hash, deptypes = elt['hash'], elt['type']
            else:
                raise SpecError("Couldn't parse dependency types in spec.")

            yield dep_name, dag_hash, list(deptypes)

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
            raise SpecError("YAML spec contains no nodes.")
        deps = dict((spec.name, spec) for spec in dep_list)
        spec = dep_list[0]

        for node in nodes:
            # get dependency dict from the node.
            name = next(iter(node))

            if 'dependencies' not in node[name]:
                continue

            yaml_deps = node[name]['dependencies']
            for dname, dhash, dtypes in Spec.read_yaml_dep_specs(yaml_deps):
                # Fill in dependencies by looking them up by name in deps dict
                deps[name]._dependencies[dname] = DependencySpec(
                    deps[name], deps[dname], dtypes)

        return spec

    @staticmethod
    def from_yaml(stream):
        """Construct a spec from YAML.

        Parameters:
        stream -- string or file object to read from.
        """
        try:
            data = syaml.load(stream)
            return Spec.from_dict(data)
        except MarkedYAMLError as e:
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
            raise sjson.SpackJSONError("error parsing JSON spec:", str(e))

    def _concretize_helper(self, presets=None, visited=None):
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
        visited.add(self.name)

        if self.external:
            return False

        changed = False

        # Concretize deps first -- this is a bottom-up process.
        for name in sorted(self._dependencies.keys()):
            changed |= self._dependencies[
                name].spec._concretize_helper(presets, visited)

        if self.name in presets:
            changed |= self.constrain(presets[self.name])
        else:
            # Concretize virtual dependencies last.  Because they're added
            # to presets below, their constraints will all be merged, but we'll
            # still need to select a concrete package later.
            if not self.virtual:
                changed |= any(
                    (spack.concretizer.concretize_architecture(self),
                     spack.concretizer.concretize_compiler(self),
                     spack.concretizer.concretize_compiler_flags(
                         self),  # has to be concretized after compiler
                     spack.concretizer.concretize_version(self),
                     spack.concretizer.concretize_variants(self)))
            presets[self.name] = self

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

    def _expand_virtual_packages(self):
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
        self_index = ProviderIndex(self.traverse(), restrict=True)
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
                    candidates = spack.concretizer.choose_virtual_or_external(
                        spec)

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
                        except SpecError:
                            # On error, we'll try the next replacement.
                            continue

                # If replacement is external then trim the dependencies
                if replacement.external:
                    if (spec._dependencies):
                        changed = True
                        spec._dependencies = DependencyMap(spec)
                    replacement._dependencies = DependencyMap(replacement)

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
                        feq(replacement.external_module,
                            spec.external_module)):
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

    def concretize(self):
        """A spec is concrete if it describes one build of a package uniquely.
           This will ensure that this spec is concrete.

           If this spec could describe more than one version, variant, or build
           of a package, this will add constraints to make it concrete.

           Some rigorous validation and checks are also performed on the spec.
           Concretizing ensures that it is self-consistent and that it's
           consistent with requirements of its pacakges.  See flatten() and
           normalize() for more details on this.
        """
        if not self.name:
            raise SpecError("Attempting to concretize anonymous spec")

        if self._concrete:
            return

        changed = True
        force = False

        while changed:
            changes = (self.normalize(force),
                       self._expand_virtual_packages(),
                       self._concretize_helper())
            changed = any(changes)
            force = True

        for s in self.traverse(deptype_query=alldeps):
            # After concretizing, assign namespaces to anything left.
            # Note that this doesn't count as a "change".  The repository
            # configuration is constant throughout a spack run, and
            # normalize and concretize evaluate Packages using Repo.get(),
            # which respects precedence.  So, a namespace assignment isn't
            # changing how a package name would have been interpreted and
            # we can do it as late as possible to allow as much
            # compatibility across repositories as possible.
            if s.namespace is None:
                s.namespace = spack.repo.repo_for_pkg(s.name).namespace

        for s in self.traverse():
            if s.external_module:
                compiler = spack.compilers.compiler_for_spec(
                    s.compiler, s.architecture)
                for mod in compiler.modules:
                    load_module(mod)

                s.external_path = get_path_from_module(s.external_module)

        # Mark everything in the spec as concrete, as well.
        self._mark_concrete()

        # Now that the spec is concrete we should check if
        # there are declared conflicts
        matches = []
        for x in self.traverse():
            for conflict_spec, when_list in x.package.conflicts.items():
                if x.satisfies(conflict_spec):
                    for when_spec, msg in when_list:
                        if x.satisfies(when_spec):
                            matches.append((x, conflict_spec, when_spec, msg))
        if matches:
            raise ConflictsInSpecError(self, matches)

    def _mark_concrete(self, value=True):
        """Mark this spec and its dependencies as concrete.

        Only for internal use -- client code should use "concretize"
        unless there is a need to force a spec to be concrete.
        """
        for s in self.traverse(deptype_query=alldeps):
            s._normal = value
            s._concrete = value

    def concretized(self):
        """This is a non-destructive version of concretize().  First clones,
           then returns a concrete version of this package without modifying
           this package. """
        clone = self.copy()
        clone.concretize()
        return clone

    def flat_dependencies(self, **kwargs):
        """Return a DependencyMap containing all of this spec's
           dependencies with their constraints merged.

           If copy is True, returns merged copies of its dependencies
           without modifying the spec it's called on.

           If copy is False, clears this spec's dependencies and
           returns them.
        """
        copy = kwargs.get('copy', True)
        deptype_query = kwargs.get('deptype_query')

        flat_deps = {}
        try:
            deptree = self.traverse(root=False, deptype_query=deptype_query)
            for spec in deptree:

                if spec.name not in flat_deps:
                    if copy:
                        spec = spec.copy(deps=False)
                    flat_deps[spec.name] = spec
                else:
                    flat_deps[spec.name].constrain(spec)

            if not copy:
                for spec in flat_deps.values():
                    spec._dependencies.clear()
                    spec._dependents.clear()
                self._dependencies.clear()

            return flat_deps

        except UnsatisfiableSpecError as e:
            # Here, the DAG contains two instances of the same package
            # with inconsistent constraints.  Users cannot produce
            # inconsistent specs like this on the command line: the
            # parser doesn't allow it. Spack must be broken!
            raise InconsistentSpecError("Invalid Spec DAG: %s" % e.message)

    def index(self, deptype=None):
        """Return DependencyMap that points to all the dependencies in this
           spec."""
        dm = DependencyMap(None)
        for spec in self.traverse(deptype=deptype):
            dm[spec.name] = spec
        return dm

    def _evaluate_dependency_conditions(self, name):
        """Evaluate all the conditions on a dependency with this name.

        If the package depends on <name> in this configuration, return
        the dependency.  If no conditions are True (and we don't
        depend on it), return None.
        """
        pkg = spack.repo.get(self.fullname)
        conditions = pkg.dependencies[name]

        substitute_abstract_variants(self)
        # evaluate when specs to figure out constraints on the dependency.
        dep = None
        for when_spec, dep_spec in conditions.items():
            sat = self.satisfies(when_spec, strict=True)
            if sat:
                if dep is None:
                    dep = Spec(name)
                try:
                    dep.constrain(dep_spec)
                except UnsatisfiableSpecError as e:
                    e.message = ("Conflicting conditional dependencies on"
                                 "package %s for spec %s" % (self.name, self))
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

    def _merge_dependency(self, dep, deptypes, visited, spec_deps,
                          provider_index):
        """Merge the dependency into this spec.

        Caller should assume that this routine can owns the dep parameter
        (i.e. it needs to be a copy of any internal structures like
        dependencies on Package class objects).

        This is the core of normalize().  There are some basic steps:

          * If dep is virtual, evaluate whether it corresponds to an
            existing concrete dependency, and merge if so.

          * If it's real and it provides some virtual dep, see if it provides
            what some virtual dependency wants and merge if so.

          * Finally, if none of the above, merge dependency and its
            constraints into this spec.

        This method returns True if the spec was changed, False otherwise.

        """
        changed = False

        # If it's a virtual dependency, try to find an existing
        # provider in the spec, and merge that.
        if dep.virtual:
            visited.add(dep.name)
            provider = self._find_provider(dep, provider_index)
            if provider:
                dep = provider
        else:
            index = ProviderIndex([dep], restrict=True)
            items = list(spec_deps.items())
            for name, vspec in items:
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
            spec_deps[dep.name] = dep
            changed = True
        else:
            # merge package/vdep information into spec
            try:
                changed |= spec_deps[dep.name].constrain(dep)
            except UnsatisfiableSpecError as e:
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
                    e.provided
                )
                raise e

        # Add merged spec to my deps and recurse
        dependency = spec_deps[dep.name]
        if dep.name not in self._dependencies:
            self._add_dependency(dependency, deptypes)

        changed |= dependency._normalize_helper(
            visited, spec_deps, provider_index)
        return changed

    def _normalize_helper(self, visited, spec_deps, provider_index):
        """Recursive helper function for _normalize."""
        if self.name in visited:
            return False
        visited.add(self.name)

        # if we descend into a virtual spec, there's nothing more
        # to normalize.  Concretize will finish resolving it later.
        if self.virtual or self.external:
            return False

        # Combine constraints from package deps with constraints from
        # the spec, until nothing changes.
        any_change = False
        changed = True

        pkg = spack.repo.get(self.fullname)
        while changed:
            changed = False
            for dep_name in pkg.dependencies:
                # Do we depend on dep_name?  If so pkg_dep is not None.
                pkg_dep = self._evaluate_dependency_conditions(dep_name)
                deptypes = pkg.dependency_types[dep_name]
                # If pkg_dep is a dependency, merge it.
                if pkg_dep:
                    changed |= self._merge_dependency(
                        pkg_dep, deptypes, visited, spec_deps, provider_index)
            any_change |= changed

        return any_change

    def normalize(self, force=False):
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
            raise SpecError("Attempting to normalize anonymous spec")

        if self._normal and not force:
            return False

        # avoid any assumptions about concreteness when forced
        if force:
            self._mark_concrete(False)

        # Ensure first that all packages & compilers in the DAG exist.
        self.validate_or_raise()
        # Get all the dependencies into one DependencyMap
        spec_deps = self.flat_dependencies(copy=False, deptype_query=alldeps)

        # Initialize index of virtual dependency providers if
        # concretize didn't pass us one already
        provider_index = ProviderIndex(
            [s for s in spec_deps.values()], restrict=True)

        # traverse the package DAG and fill out dependencies according
        # to package files & their 'when' specs
        visited = set()

        any_change = self._normalize_helper(visited, spec_deps, provider_index)

        # If there are deps specified but not visited, they're not
        # actually deps of this package.  Raise an error.
        extra = set(spec_deps.keys()).difference(visited)
        if extra:
            raise InvalidDependencyError(
                self.name + " does not depend on " + comma_or(extra))

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
                pkg_cls = spec.package_class
                pkg_variants = pkg_cls.variants
                not_existing = set(spec.variants) - set(pkg_variants)
                if not_existing:
                    raise UnknownVariantError(spec.name, not_existing)

                substitute_abstract_variants(spec)

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
                raise UnsatisfiableSpecError(
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
                raise UnsatisfiableVariantSpecError(
                    self.variants[v], other.variants[v]
                )

        # TODO: Check out the logic here
        sarch, oarch = self.architecture, other.architecture
        if sarch is not None and oarch is not None:
            if sarch.platform is not None and oarch.platform is not None:
                if sarch.platform != oarch.platform:
                    raise UnsatisfiableArchitectureSpecError(sarch, oarch)
            if sarch.platform_os is not None and oarch.platform_os is not None:
                if sarch.platform_os != oarch.platform_os:
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
            if sarch.platform_os is None or oarch.platform_os is None:
                sarch.platform_os = sarch.platform_os or oarch.platform_os
            if sarch.target is None or oarch.target is None:
                sarch.target = sarch.target or oarch.target
        changed |= (str(self.architecture) != old)

        if deps:
            changed |= self._constrain_dependencies(other)

        return changed

    def _constrain_dependencies(self, other):
        """Apply constraints of other spec's dependencies to this spec."""
        other = self._autospec(other)

        if not self._dependencies or not other._dependencies:
            return False

        # TODO: might want more detail than this, e.g. specific deps
        # in violation. if this becomes a priority get rid of this
        # check and be more specific about what's wrong.
        if not other.satisfies_dependencies(self):
            raise UnsatisfiableDependencySpecError(other, self)

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
        # XXX(deptype): handle deptypes via deptype kwarg.
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
        if isinstance(spec_like, spack.spec.Spec):
            return spec_like

        try:
            spec = spack.spec.Spec(spec_like)
            if not spec.name:
                raise SpecError(
                    "anonymous package -- this will always be handled")
            return spec
        except SpecError:
            return parse_anonymous_spec(spec_like, self.name)

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
            except spack.repository.UnknownEntityError:
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

        if strict:
            if other._dependencies and not self._dependencies:
                return False

            selfdeps = self.traverse(root=False)
            otherdeps = other.traverse(root=False)
            if not all(any(d.satisfies(dep) for d in selfdeps)
                       for dep in otherdeps):
                return False

        elif not self._dependencies or not other._dependencies:
            # if either spec doesn't restrict dependencies then both are
            # compatible.
            return True

        # Handle first-order constraints directly
        for name in self.common_dependencies(other):
            if not self[name].satisfies(other[name], deps=False):
                return False

        # For virtual dependencies, we need to dig a little deeper.
        self_index = ProviderIndex(self.traverse(), restrict=True)
        other_index = ProviderIndex(other.traverse(), restrict=True)

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

    def _dup(self, other, deps=True, cleardeps=True):
        """Copy the spec other into self.  This is an overwriting
        copy.  It does not copy any dependents (parents), but by default
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
                       self.external_module != other.external_module and
                       self.compiler_flags != other.compiler_flags)

        # Local node attributes get copied first.
        self.name = other.name
        self.versions = other.versions.copy()
        self.architecture = other.architecture.copy() if other.architecture \
            else None
        self.compiler = other.compiler.copy() if other.compiler else None
        if cleardeps:
            self._dependents = DependencyMap(self)
            self._dependencies = DependencyMap(self)
        self.compiler_flags = other.compiler_flags.copy()
        self.compiler_flags.spec = self
        self.variants = other.variants.copy()
        self.variants.spec = self
        self.external_path = other.external_path
        self.external_module = other.external_module
        self.namespace = other.namespace

        # If we copy dependencies, preserve DAG structure in the new spec
        if deps:
            deptypes = alldeps  # by default copy all deptypes

            # if caller restricted deptypes to be copied, adjust that here.
            if isinstance(deps, (tuple, list)):
                deptypes = deps

            self._dup_deps(other, deptypes)

        # These fields are all cached results of expensive operations.
        # If we preserved the original structure, we can copy them
        # safely. If not, they need to be recomputed.
        # TODO: dependency hashes can be copied more aggressively.
        if deps is True or deps == alldeps:
            self._hash = other._hash
            self._cmp_key_cache = other._cmp_key_cache
            self._normal = other._normal
            self._concrete = other._concrete
        else:
            self._hash = None
            self._cmp_key_cache = None
            self._normal = False
            self._concrete = False

        return changed

    def _dup_deps(self, other, deptypes):
        new_specs = {self.name: self}
        for dspec in other.traverse_edges(cover='edges', root=False):
            if (dspec.deptypes and
                not any(d in deptypes for d in dspec.deptypes)):
                continue

            if dspec.parent.name not in new_specs:
                new_specs[dspec.parent.name] = dspec.parent.copy(deps=False)
            if dspec.spec.name not in new_specs:
                new_specs[dspec.spec.name] = dspec.spec.copy(deps=False)

            new_specs[dspec.parent.name]._add_dependency(
                new_specs[dspec.spec.name], dspec.deptypes)

    def copy(self, deps=True):
        """Return a copy of this spec.

        By default, returns a deep copy. To control how dependencies are
        copied, supply:

        deps=True:  deep copy

        deps=False: shallow copy (no dependencies)

        deps=('link', 'build'):
            only build and link dependencies.  Similar for other deptypes.

        """
        clone = Spec.__new__(Spec)
        clone._dup(self, deps=deps)
        return clone

    @property
    def version(self):
        if not self.versions.concrete:
            raise SpecError("Spec version is not concrete: " + str(self))
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
        """True if this spec satisfies the provided spec, or if any dependency
           does.  If the spec has no name, then we parse this one first.
        """
        spec = self._autospec(spec)
        for s in self.traverse():
            if s.satisfies(spec, strict=True):
                return True

        return False

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
        return (self.name,
                self.namespace,
                self.versions,
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

    def format(self, format_string='$_$@$%@+$+$=', **kwargs):
        """
        Prints out particular pieces of a spec, depending on what is
        in the format string.  The format strings you can provide are::

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
            ${VERSION}       Version
            ${COMPILER}      Full compiler string
            ${COMPILERNAME}  Compiler name
            ${COMPILERVER}   Compiler version
            ${COMPILERFLAGS} Compiler flags
            ${OPTIONS}       Options
            ${ARCHITECTURE}  Architecture
            ${SHA1}          Dependencies 8-char sha1 prefix
            ${HASH:len}      DAG hash with optional length specifier

            ${SPACK_ROOT}    The spack root directory
            ${SPACK_INSTALL} The default spack install directory,
                             ${SPACK_PREFIX}/opt
            ${PREFIX}        The package prefix

        Note these are case-insensitive: for example you can specify either
        ``${PACKAGE}`` or ``${package}``.

        Optionally you can provide a width, e.g. ``$20_`` for a 20-wide name.
        Like printf, you can provide '-' for left justification, e.g.
        ``$-20_`` for a left-justified name.

        Anything else is copied verbatim into the output stream.

        *Example:*  ``$_$@$+`` translates to the name, version, and options
        of the package, but no dependencies, arch, or compiler.

        TODO: allow, e.g., ``$6#`` to customize short hash length
        TODO: allow, e.g., ``$//`` for full hash.
        """
        color = kwargs.get('color', False)
        length = len(format_string)
        out = StringIO()
        named = escape = compiler = False
        named_str = fmt = ''

        def write(s, c):
            f = color_formats[c] + cescape(s) + '@.'
            cwrite(f, stream=out, color=color)

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
                    out.write(fmt % self.fullname)
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
                if named_str == 'PACKAGE':
                    name = self.name if self.name else ''
                    write(fmt % self.name, '@')
                if named_str == 'VERSION':
                    if self.versions and self.versions != _any_version:
                        write(fmt % str(self.versions), '@')
                elif named_str == 'COMPILER':
                    if self.compiler:
                        write(fmt % self.compiler, '%')
                elif named_str == 'COMPILERNAME':
                    if self.compiler:
                        write(fmt % self.compiler.name, '%')
                elif named_str in ['COMPILERVER', 'COMPILERVERSION']:
                    if self.compiler:
                        write(fmt % self.compiler.versions, '%')
                elif named_str == 'COMPILERFLAGS':
                    if self.compiler:
                        write(fmt % str(self.compiler_flags), '%')
                elif named_str == 'OPTIONS':
                    if self.variants:
                        write(fmt % str(self.variants), '+')
                elif named_str == 'ARCHITECTURE':
                    if self.architecture and str(self.architecture):
                        write(fmt % str(self.architecture), '=')
                elif named_str == 'SHA1':
                    if self.dependencies:
                        out.write(fmt % str(self.dag_hash(7)))
                elif named_str == 'SPACK_ROOT':
                    out.write(fmt % spack.prefix)
                elif named_str == 'SPACK_INSTALL':
                    out.write(fmt % spack.store.root)
                elif named_str == 'PREFIX':
                    out.write(fmt % self.prefix)
                elif named_str.startswith('HASH'):
                    if named_str.startswith('HASH:'):
                        _, hashlen = named_str.split(':')
                        hashlen = int(hashlen)
                    else:
                        hashlen = None
                    out.write(fmt % (self.dag_hash(hashlen)))

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
        return ''.join("^" + dep.format() for dep in self.sorted_deps())

    def __str__(self):
        ret = self.format() + self.dep_string()
        return ret.strip()

    def _install_status(self):
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
        color = kwargs.pop('color', get_color_when())
        depth = kwargs.pop('depth', False)
        hashes = kwargs.pop('hashes', False)
        hlen = kwargs.pop('hashlen', None)
        install_status = kwargs.pop('install_status', False)
        cover = kwargs.pop('cover', 'nodes')
        indent = kwargs.pop('indent', 0)
        fmt = kwargs.pop('format', '$_$@$%@+$+$=')
        prefix = kwargs.pop('prefix', None)
        show_types = kwargs.pop('show_types', False)
        deptypes = kwargs.pop('deptypes', ('build', 'link'))
        check_kwargs(kwargs, self.tree)

        out = ""
        for d, dep_spec in self.traverse_edges(
                order='pre', cover=cover, depth=True, deptypes=deptypes):
            node = dep_spec.spec

            if prefix is not None:
                out += prefix(node)
            out += " " * indent

            if depth:
                out += "%-4d" % d

            if install_status:
                status = node._install_status()
                if status is None:
                    out += "     "  # Package isn't installed
                elif status:
                    out += colorize("@g{[+]}  ", color=color)  # installed
                else:
                    out += colorize("@r{[-]}  ", color=color)  # missing

            if hashes:
                out += colorize('@K{%s}  ', color=color) % node.dag_hash(hlen)

            if show_types:
                out += '['
                if dep_spec.deptypes:
                    for t in alldeps:
                        out += ''.join(t[0] if t in dep_spec.deptypes else ' ')
                else:
                    out += ' ' * len(alldeps)
                out += ']  '

            out += ("    " * d)
            if d > 0:
                out += "^"
            out += node.format(fmt, color=color) + "\n"
        return out

    def __repr__(self):
        return str(self)


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


#
# These are possible token types in the spec grammar.
#
HASH, DEP, AT, COLON, COMMA, ON, OFF, PCT, EQ, ID, VAL = range(11)


class SpecLexer(spack.parse.Lexer):

    """Parses tokens that make up spack specs."""

    def __init__(self):
        super(SpecLexer, self).__init__([
            (r'/', lambda scanner, val: self.token(HASH,  val)),
            (r'\^', lambda scanner, val: self.token(DEP,   val)),
            (r'\@', lambda scanner, val: self.token(AT,    val)),
            (r'\:', lambda scanner, val: self.token(COLON, val)),
            (r'\,', lambda scanner, val: self.token(COMMA, val)),
            (r'\+', lambda scanner, val: self.token(ON,    val)),
            (r'\-', lambda scanner, val: self.token(OFF,   val)),
            (r'\~', lambda scanner, val: self.token(OFF,   val)),
            (r'\%', lambda scanner, val: self.token(PCT,   val)),
            (r'\=', lambda scanner, val: self.token(EQ,    val)),
            # This is more liberal than identifier_re (see above).
            # Checked by check_identifier() for better error messages.
            (r'\w[\w.-]*', lambda scanner, val: self.token(ID,    val)),
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
                # TODO: clean this parsing up a bit
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
                        if self.accept(HASH):
                            # We're finding a dependency by hash for an
                            # anonymous spec
                            dep = self.spec_by_hash()
                        else:
                            # We're adding a dependency to the last spec
                            self.expect(ID)
                            dep = self.spec(self.token.value)

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

        # If the spec has an os or a target and no platform, give it
        # the default platform
        platform_default = spack.architecture.platform().name
        for spec in specs:
            for s in spec.traverse():
                if s.architecture and not s.architecture.platform and \
                        (s.architecture.platform_os or s.architecture.target):
                    s._set_architecture(platform=platform_default)
        return specs

    def parse_compiler(self, text):
        self.setup(text)
        return self.compiler()

    def spec_by_hash(self):
        self.expect(ID)

        specs = spack.store.db.query()
        matches = [spec for spec in specs if
                   spec.dag_hash()[:len(self.token.value)] == self.token.value]

        if not matches:
            raise NoSuchHashError(self.token.value)

        if len(matches) != 1:
            raise AmbiguousHashError(
                "Multiple packages specify hash beginning '%s'."
                % self.token.value, *matches)

        return matches[0]

    def spec(self, name):
        """Parse a spec out of the input. If a spec is supplied, initialize
           and return it instead of creating a new one."""
        if name:
            spec_namespace, dot, spec_name = name.rpartition('.')
            if not spec_namespace:
                spec_namespace = None
            self.check_identifier(spec_name)
        else:
            spec_namespace = None
            spec_name = None

        if self._initial is None:
            # This will init the spec without calling Spec.__init__
            spec = Spec.__new__(Spec)
        else:
            # this is used by Spec.__init__
            spec = self._initial
            self._initial = None

        spec.name = spec_name
        spec.versions = VersionList()
        spec.variants = VariantMap(spec)
        spec.architecture = None
        spec.compiler = None
        spec.external_path = None
        spec.external_module = None
        spec.compiler_flags = FlagMap(spec)
        spec._dependents = DependencyMap(spec)
        spec._dependencies = DependencyMap(spec)
        spec.namespace = spec_namespace
        spec._hash = None
        spec._cmp_key_cache = None

        spec._normal = False
        spec._concrete = False

        # record this so that we know whether version is
        # unspecified or not.
        added_version = False

        while self.next:
            if self.accept(AT):
                vlist = self.version_list()
                for version in vlist:
                    spec._add_version(version)
                added_version = True

            elif self.accept(ON):
                name = self.variant()
                spec.variants[name] = BoolValuedVariant(name, True)

            elif self.accept(OFF):
                name = self.variant()
                spec.variants[name] = BoolValuedVariant(name, False)

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

        # If there was no version in the spec, consier it an open range
        if not added_version and not spec._hash:
            spec.versions = VersionList(':')

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
            return Version(start)
        else:
            # No colon and no id: invalid version.
            self.next_token_error("Invalid version specifier")

        if start:
            start = Version(start)
        if end:
            end = Version(end)
        return VersionRange(start, end)

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
        compiler.versions = VersionList()
        if self.accept(AT):
            vlist = self.version_list()
            for version in vlist:
                compiler._add_version(version)
        else:
            compiler.versions = VersionList(':')
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


def parse_anonymous_spec(spec_like, pkg_name):
    """Allow the user to omit the package name part of a spec if they
       know what it has to be already.

       e.g., provides('mpi@2', when='@1.9:') says that this package
       provides MPI-3 when its version is higher than 1.9.
    """
    if not isinstance(spec_like, (str, Spec)):
        raise TypeError('spec must be Spec or spec string.  Found %s'
                        % type(spec_like))

    if isinstance(spec_like, str):
        try:
            anon_spec = Spec(spec_like)
            if anon_spec.name != pkg_name:
                raise SpecParseError(spack.parse.ParseError(
                    "",
                    "",
                    "Expected anonymous spec for package %s but found spec for"
                    "package %s" % (pkg_name, anon_spec.name)))
        except SpecParseError:
            anon_spec = Spec(pkg_name + ' ' + spec_like)
            if anon_spec.name != pkg_name:
                raise ValueError(
                    "Invalid spec for package %s: %s" % (pkg_name, spec_like))
    else:
        anon_spec = spec_like.copy()

    if anon_spec.name != pkg_name:
        raise ValueError("Spec name '%s' must match package name '%s'"
                         % (anon_spec.name, pkg_name))

    return anon_spec


def base32_prefix_bits(hash_string, bits):
    """Return the first <bits> bits of a base32 string as an integer."""
    if bits > len(hash_string) * 5:
        raise ValueError("Too many bits! Requested %d bit prefix of '%s'."
                         % (bits, hash_string))

    hash_bytes = base64.b32decode(hash_string, casefold=True)
    return prefix_bits(hash_bytes, bits)


class SpecParseError(SpecError):
    """Wrapper for ParseError for when we're parsing specs."""
    def __init__(self, parse_error):
        super(SpecParseError, self).__init__(parse_error.message)
        self.string = parse_error.string
        self.pos = parse_error.pos


class DuplicateDependencyError(SpecError):
    """Raised when the same dependency occurs in a spec twice."""


class DuplicateCompilerSpecError(SpecError):
    """Raised when the same compiler occurs in a spec twice."""


class UnsupportedCompilerError(SpecError):
    """Raised when the user asks for a compiler spack doesn't know about."""
    def __init__(self, compiler_name):
        super(UnsupportedCompilerError, self).__init__(
            "The '%s' compiler is not yet supported." % compiler_name)


class DuplicateArchitectureError(SpecError):
    """Raised when the same architecture occurs in a spec twice."""


class InconsistentSpecError(SpecError):
    """Raised when two nodes in the same spec DAG have inconsistent
       constraints."""


class InvalidDependencyError(SpecError):
    """Raised when a dependency in a spec is not actually a dependency
       of the package."""


class NoProviderError(SpecError):
    """Raised when there is no package that provides a particular
       virtual dependency.
    """
    def __init__(self, vpkg):
        super(NoProviderError, self).__init__(
            "No providers found for virtual package: '%s'" % vpkg)
        self.vpkg = vpkg


class MultipleProviderError(SpecError):
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


class UnsatisfiableSpecNameError(UnsatisfiableSpecError):
    """Raised when two specs aren't even for the same package."""
    def __init__(self, provided, required):
        super(UnsatisfiableSpecNameError, self).__init__(
            provided, required, "name")


class UnsatisfiableVersionSpecError(UnsatisfiableSpecError):
    """Raised when a spec version conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableVersionSpecError, self).__init__(
            provided, required, "version")


class UnsatisfiableCompilerSpecError(UnsatisfiableSpecError):
    """Raised when a spec comiler conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableCompilerSpecError, self).__init__(
            provided, required, "compiler")


class UnsatisfiableCompilerFlagSpecError(UnsatisfiableSpecError):
    """Raised when a spec variant conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableCompilerFlagSpecError, self).__init__(
            provided, required, "compiler_flags")


class UnsatisfiableArchitectureSpecError(UnsatisfiableSpecError):
    """Raised when a spec architecture conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableArchitectureSpecError, self).__init__(
            provided, required, "architecture")


class UnsatisfiableProviderSpecError(UnsatisfiableSpecError):
    """Raised when a provider is supplied but constraints don't match
       a vpkg requirement"""
    def __init__(self, provided, required):
        super(UnsatisfiableProviderSpecError, self).__init__(
            provided, required, "provider")


# TODO: get rid of this and be more specific about particular incompatible
# dep constraints
class UnsatisfiableDependencySpecError(UnsatisfiableSpecError):
    """Raised when some dependency of constrained specs are incompatible"""
    def __init__(self, provided, required):
        super(UnsatisfiableDependencySpecError, self).__init__(
            provided, required, "dependency")


class AmbiguousHashError(SpecError):
    def __init__(self, msg, *specs):
        specs_str = '\n  ' + '\n  '.join(spec.format('$.$@$%@+$+$=$/')
                                         for spec in specs)
        super(AmbiguousHashError, self).__init__(msg + specs_str)


class InvalidHashError(SpecError):
    def __init__(self, spec, hash):
        super(InvalidHashError, self).__init__(
            "The spec specified by %s does not match provided spec %s"
            % (hash, spec))


class NoSuchHashError(SpecError):
    def __init__(self, hash):
        super(NoSuchHashError, self).__init__(
            "No installed spec matches the hash: '%s'"
            % hash)


class RedundantSpecError(SpecError):
    def __init__(self, spec, addition):
        super(RedundantSpecError, self).__init__(
            "Attempting to add %s to spec %s which is already concrete."
            " This is likely the result of adding to a spec specified by hash."
            % (addition, spec))


class ConflictsInSpecError(SpecError, RuntimeError):
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
