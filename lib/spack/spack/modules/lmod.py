##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import os.path
import llnl.util.lang as lang
import spack.compilers
import spack.spec
import spack.error
import itertools
import collections
import spack.tengine as tengine

from .common import BaseConfiguration, BaseFileLayout
from .common import BaseContext, BaseModuleFileWriter, configuration

#: LMOD specific part of the configuration
configuration = configuration.get('lmod', {})

#: Caches the configuration {spec_hash: configuration}
configuration_registry = {}


def make_configuration(spec):
    """Returns the tcl configuration for spec"""
    key = spec.dag_hash()
    try:
        return configuration_registry[key]
    except KeyError:
        return configuration_registry.setdefault(key, LmodConfiguration(spec))


def make_layout(spec):
    """Returns the layout information for spec """
    conf = make_configuration(spec)
    return LmodFileLayout(conf)


def make_context(spec):
    """Returns the context information for spec"""
    conf = make_configuration(spec)
    return LmodContext(conf)


class LmodConfiguration(BaseConfiguration):
    """Configuration class for lmod module files."""

    @property
    def core_compilers(self):
        """Returns the list of "Core" compilers

        :raises CoreCompilersNotFoundError: if the key was not
            specified in the configuration file or the sequence
            is empty
        """
        value = configuration.get('core_compilers')
        if value is None:
            msg = '\'core_compilers\' key not found in configuration file'
            raise CoreCompilersNotFoundError(msg)
        if not value:
            msg = '\'core_compilers\' list cannot be empty'
            raise CoreCompilersNotFoundError(msg)
        return value

    @property
    def hierarchy_tokens(self):
        """Returns the list of tokens that are part of the modulefile
        hierarchy. 'compiler' is always present.
        """
        tokens = configuration.get('hierarchy', [])

        # Check if all the tokens in the hierarchy are virtual specs.
        # If not warn the user and raise an error.
        not_virtual = [t for t in tokens if not spack.spec.Spec.is_virtual(t)]
        if not_virtual:
            msg = "Non-virtual specs in 'hierarchy' list for lmod: {0}\n"
            msg += "Please check the 'modules.yaml' configuration files"
            msg.format(', '.join(not_virtual))
            raise NonVirtualInHierarchyError(msg)

        # Append 'compiler' which is always implied
        tokens.append('compiler')

        # Deduplicate tokens in case duplicates have been coded
        tokens = list(lang.dedupe(tokens))

        return tokens

    @property
    def requires(self):
        """Returns a dictionary mapping all the requirements of this spec
        to the actual provider. 'compiler' is always present among the
        requirements.
        """
        # Keep track of the requirements that this package has in terms
        # of virtual packages that participate in the hierarchical structure
        requirements = {'compiler': self.spec.compiler}
        # For each virtual dependency in the hierarchy
        for x in self.hierarchy_tokens:
            # If I depend on it
            if x in self.spec and not self.spec.package.provides(x):
                requirements[x] = self.spec[x]  # record the actual provider
        return requirements

    @property
    def provides(self):
        """Returns a dictionary mapping all the services provided by this
        spec to the spec itself.
        """
        provides = {}

        # Treat the 'compiler' case in a special way, as compilers are not
        # virtual dependencies in spack

        # If it is in the list of supported compilers family -> compiler
        if self.spec.name in spack.compilers.supported_compilers():
            provides['compiler'] = spack.spec.CompilerSpec(str(self.spec))
        # Special case for llvm
        if self.spec.name == 'llvm':
            provides['compiler'] = spack.spec.CompilerSpec(str(self.spec))
            provides['compiler'].name = 'clang'

        # All the other tokens in the hierarchy must be virtual dependencies
        for x in self.hierarchy_tokens:
            if self.spec.package.provides(x):
                provides[x] = self.spec[x]
        return provides

    @property
    def available(self):
        """Returns a dictionary of the services that are currently
        available.
        """
        available = {}
        # What is available is what I require plus what I provide.
        # 'compiler' is the only key that may be overridden.
        available.update(self.requires)
        available.update(self.provides)
        return available

    @property
    def missing(self):
        """Returns the list of tokens that are not available."""
        return [x for x in self.hierarchy_tokens if x not in self.available]


class LmodFileLayout(BaseFileLayout):
    """File layout for lmod module files."""

    #: file extension of lua module files
    extension = 'lua'

    @property
    def filename(self):
        """Returns the filename for the current module file"""

        # Get the list of requirements and build an **ordered**
        # list of the path parts
        requires = self.conf.requires
        hierarchy = self.conf.hierarchy_tokens
        path_parts = lambda x: self.token_to_path(x, requires[x])
        parts = [path_parts(x) for x in hierarchy if x in requires]

        # My relative path if just a join of all the parts
        hierarchy_name = os.path.join(*parts)

        # Compute the absolute path
        fullname = os.path.join(
            self.dirname(),  # root for lmod module files
            hierarchy_name,  # relative path
            '.'.join([self.use_name, self.extension])  # file name
        )
        return fullname

    @property
    def use_name(self):
        """Returns the 'use' name of the module i.e. the name you have to type
        to console to use it.
        """
        # Package name and version
        base = os.path.join("${PACKAGE}", "${VERSION}")
        name_parts = [self.spec.format(base)]
        # The remaining elements are filename suffixes
        name_parts.extend(self.conf.suffixes)
        return '-'.join(name_parts)

    def token_to_path(self, name, value):
        """Transforms a hierarchy token into the corresponding path part.

        :param str name: name of the service in the hierarchy
        :param value: actual provider of the service
        :return: part of the path associated with the service
        :rtype: str
        """
        # General format for the path part
        path_part_fmt = os.path.join('{token.name}', '{token.version}')

        # If we are dealing with a core compiler, return 'Core'
        core_compilers = self.conf.core_compilers
        if name == 'compiler' and str(value) in core_compilers:
            return 'Core'

        # CompilerSpec does not have an hash, as we are not allowed to
        # use different flavors of the same compiler
        if name == 'compiler':
            return path_part_fmt.format(token=value)

        # In case the hierarchy token refers to a virtual provider
        # we need to append an hash to the version to distinguish
        # among flavors of the same library (e.g. openblas~openmp vs.
        # openblas+openmp)
        path = path_part_fmt.format(token=value)
        path = '-'.join([path, value.dag_hash(length=7)])
        return path

    @property
    def available_path_parts(self):
        """List of path parts that are currently available. Needed to
        construct the file name.
        """
        # List of available services
        available = self.conf.available
        # List of services that are part of the hierarchy
        hierarchy = self.conf.hierarchy_tokens
        # List of items that are both in the hierarchy and available
        l = [x for x in hierarchy if x in available]
        # Tokenize each part
        parts = [self.token_to_path(x, available[x]) for x in l]
        return parts

    @property
    def unlocked_paths(self):
        """Returns a dictionary mapping conditions to a list of unlocked
        paths. The paths that are unconditionally unlocked are under the
        key 'None'. The other keys represent the list of services you need
        loaded to unlock the corresponding paths.
        """

        unlocked = collections.defaultdict(list)

        # Get the list of services we require and we provide
        requires_key = list(self.conf.requires)
        provides_key = list(self.conf.provides)

        # A compiler is always required. To avoid duplication pop the
        # 'compiler' item from required if we also **provide** one
        if 'compiler' in provides_key:
            requires_key.remove('compiler')

        # Compute the unique combinations of the services we provide
        combinations = []
        for ii in range(len(provides_key)):
            combinations += itertools.combinations(provides_key, ii + 1)

        # Attach the services required to each combination
        to_be_processed = [x + tuple(requires_key) for x in combinations]

        # Compute the paths that are unconditionally added
        # and append them to the dictionary (key = None)
        available_combination = []
        for item in to_be_processed:
            hierarchy = self.conf.hierarchy_tokens
            available = self.conf.available
            l = [x for x in hierarchy if x in item]
            available_combination.append(tuple(l))
            parts = [self.token_to_path(x, available[x]) for x in l]
            unlocked[None].append(tuple([self.dirname()] + parts))

        # Deduplicate the list
        unlocked[None] = list(lang.dedupe(unlocked[None]))

        # Compute the combination of missing requirements: this will lead to
        # paths that are unlocked conditionally
        missing = self.conf.missing

        missing_combinations = []
        for ii in range(len(missing)):
            missing_combinations += itertools.combinations(missing, ii + 1)

        # Attach the services required to each combination
        for m in missing_combinations:
            to_be_processed = [m + x for x in available_combination]
            for item in to_be_processed:
                hierarchy = self.conf.hierarchy_tokens
                available = self.conf.available
                token2path = lambda x: self.token_to_path(x, available[x])
                l = [x for x in hierarchy if x in item]
                parts = []
                for x in l:
                    value = token2path(x) if x in available else x
                    parts.append(value)
                unlocked[m].append(tuple([self.dirname()] + parts))
            # Deduplicate the list
            unlocked[m] = list(lang.dedupe(unlocked[m]))
        return unlocked


class LmodContext(BaseContext):
    """Context class for lmod module files."""

    @tengine.context_property
    def has_modulepath_modifications(self):
        """True if this module modifies MODULEPATH, False otherwise."""
        return bool(self.conf.provides)

    @tengine.context_property
    def has_conditional_modifications(self):
        """True if this module modifies MODULEPATH conditionally to the
        presence of other services in the environment, False otherwise.
        """
        # In general we have conditional modifications if we have modifications
        # and we are not providing **only** a compiler
        provides = self.conf.provides
        provide_compiler_only = 'compiler' in provides and len(provides) == 1
        has_modifications = self.has_modulepath_modifications
        return has_modifications and not provide_compiler_only

    @tengine.context_property
    def name_part(self):
        """Name of this provider."""
        return self.spec.name

    @tengine.context_property
    def version_part(self):
        """Version of this provider."""
        s = self.spec
        return '-'.join([str(s.version), s.dag_hash(length=7)])

    @tengine.context_property
    def provides(self):
        """Returns the dictionary of provided services."""
        return self.conf.provides

    @tengine.context_property
    def missing(self):
        """Returns a list of missing services."""
        return self.conf.missing

    @tengine.context_property
    def unlocked_paths(self):
        """Returns the list of paths that are unlocked unconditionally."""
        l = make_layout(self.spec)
        return [os.path.join(*parts) for parts in l.unlocked_paths[None]]

    @tengine.context_property
    def conditionally_unlocked_paths(self):
        """Returns the list of paths that are unlocked conditionally.
        Each item in the list is a tuple with the structure (condition, path).
        """
        l = make_layout(self.spec)
        value = []
        conditional_paths = l.unlocked_paths
        conditional_paths.pop(None)
        for services_needed, list_of_path_parts in conditional_paths.items():
            condition = ' and '.join([x + '_name' for x in services_needed])
            for parts in list_of_path_parts:

                def manipulate_path(token):
                    if token in self.conf.hierarchy_tokens:
                        return '{0}_name, {0}_version'.format(token)
                    return '"' + token + '"'

                path = ', '.join([manipulate_path(x) for x in parts])

                value.append((condition, path))
        return value


class LmodModulefileWriter(BaseModuleFileWriter):
    """Writer class for lmod module files."""
    default_template = os.path.join('modules', 'modulefile.lua')


class CoreCompilersNotFoundError(spack.error.SpackError, KeyError):
    """Error raised if the key 'core_compilers' has not been specified
    in the configuration file.
    """
    pass


class NonVirtualInHierarchyError(spack.error.SpackError, TypeError):
    """Error raised if non-virtual specs are used as hierarchy tokens in
    the lmod section of 'modules.yaml'.
    """
