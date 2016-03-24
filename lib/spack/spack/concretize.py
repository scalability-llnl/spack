##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""
Functions here are used to take abstract specs and make them concrete.
For example, if a spec asks for a version between 1.8 and 1.9, these
functions might take will take the most recent 1.9 version of the
package available.  Or, if the user didn't specify a compiler for a
spec, then this will assign a compiler to the spec based on defaults
or user preferences.

TODO: make this customizable and allow users to configure
      concretization  policies.
"""
import spack
import spack.spec
import spack.compilers
import spack.architecture
import spack.error
from spack.version import *
from functools import partial
from spec import DependencyMap
from itertools import chain
from spack.config import *

class DefaultConcretizer(object):
    """This class doesn't have any state, it just provides some methods for
       concretization.  You can subclass it to override just some of the
       default concretization strategies, or you can override all of them.
    """

    def _valid_virtuals_and_externals(self, spec):
        """Returns a list of candidate virtual dep providers and external
           packages that coiuld be used to concretize a spec."""
        # First construct a list of concrete candidates to replace spec with.
        candidates = [spec]
        if spec.virtual:
            providers = spack.repo.providers_for(spec)
            if not providers:
                raise UnsatisfiableProviderSpecError(providers[0], spec)
            spec_w_preferred_providers = find_spec(
                spec, lambda(x): spack.pkgsort.spec_has_preferred_provider(x.name, spec.name))
            if not spec_w_preferred_providers:
                spec_w_preferred_providers = spec
            provider_cmp = partial(spack.pkgsort.provider_compare, spec_w_preferred_providers.name, spec.name)
            candidates = sorted(providers, cmp=provider_cmp)

        # For each candidate package, if it has externals, add those to the usable list.
        # if it's not buildable, then *only* add the externals.
        usable = []
        for cspec in candidates:
            if is_spec_buildable(cspec):
                usable.append(cspec)
            externals = spec_externals(cspec)
            for ext in externals:
                if ext.satisfies(spec):
                    usable.append(ext)

        # If nothing is in the usable list now, it's because we aren't
        # allowed to build anything.
        if not usable:
            raise NoBuildError(spec)

        def cmp_externals(a, b):
            if a.name != b.name:
                # We're choosing between different providers, so
                # maintain order from provider sort
                return candidates.index(a) - candidates.index(b)

            result = cmp_specs(a, b)
            if result != 0:
                return result

            # prefer external packages to internal packages.
            if a.external is None or b.external is None:
                return -cmp(a.external, b.external)
            else:
                return cmp(a.external, b.external)

        usable.sort(cmp=cmp_externals)
        return usable


    def choose_virtual_or_external(self, spec):
        """Given a list of candidate virtual and external packages, try to
           find one that is most ABI compatible.
        """
        candidates = self._valid_virtuals_and_externals(spec)
        if not candidates:
            return candidates

        # Find the nearest spec in the dag that has a compiler.  We'll
        # use that spec to calibrate compiler compatibility.
        abi_exemplar = find_spec(spec, lambda(x): x.compiler)
        if not abi_exemplar:
            abi_exemplar = spec.root

        # Make a list including ABI compatibility of specs with the exemplar.
        strict = [spack.abi.compatible(c, abi_exemplar) for c in candidates]
        loose  = [spack.abi.compatible(c, abi_exemplar, loose=True) for c in candidates]
        keys = zip(strict, loose, candidates)

        # Sort candidates from most to least compatibility.
        # Note:
        #   1. We reverse because True > False.
        #   2. Sort is stable, so c's keep their order.
        keys.sort(key=lambda k:k[:2], reverse=True)

        # Pull the candidates back out and return them in order
        candidates = [c for s,l,c in keys]
        return candidates


    def concretize_version(self, spec):
        """If the spec is already concrete, return.  Otherwise take
           the preferred version from spackconfig, and default to the package's
           version if there are no available versions.

           TODO: In many cases we probably want to look for installed
                 versions of each package and use an installed version
                 if we can link to it.  The policy implemented here will
                 tend to rebuild a lot of stuff becasue it will prefer
                 a compiler in the spec to any compiler already-
                 installed things were built with.  There is likely
                 some better policy that finds some middle ground
                 between these two extremes.
        """
        # return if already concrete.
        if spec.versions.concrete:
            return False

        # If there are known available versions, return the most recent
        # version that satisfies the spec
        pkg = spec.package
        cmp_versions = partial(spack.pkgsort.version_compare, spec.name)
        valid_versions = sorted(
            [v for v in pkg.versions
             if any(v.satisfies(sv) for sv in spec.versions)],
            cmp=cmp_versions)

        def prefer_key(v):
            return pkg.versions.get(Version(v)).get('preferred', False)
        valid_versions.sort(key=prefer_key, reverse=True)

        if valid_versions:
            spec.versions = ver([valid_versions[0]])
        else:
            # We don't know of any SAFE versions that match the given
            # spec.  Grab the spec's versions and grab the highest
            # *non-open* part of the range of versions it specifies.
            # Someone else can raise an error if this happens,
            # e.g. when we go to fetch it and don't know how.  But it
            # *might* work.
            if not spec.versions or spec.versions == VersionList([':']):
                raise NoValidVersionError(spec)
            else:
                last = spec.versions[-1]
                if isinstance(last, VersionRange):
                    if last.end:
                        spec.versions = ver([last.end])
                    else:
                        spec.versions = ver([last.start])
                else:
                    spec.versions = ver([last])

        return True   # Things changed


    def concretize_architecture(self, spec):
        """If the spec already had an architecture, return.  Otherwise if
           the root of the DAG has an architecture, then use that.
           Otherwise take the system's default architecture.

           Intuition: Architectures won't be set a lot, and generally you
           want the host system's architecture.  When architectures are
           mised in a spec, it is likely because the tool requries a
           cross-compiled component, e.g. for tools that run on BlueGene
           or Cray machines.  These constraints will likely come directly
           from packages, so require the user to be explicit if they want
           to mess with the architecture, and revert to the default when
           they're not explicit.
        """
        if spec.architecture is not None:
            return False

        if spec.root.architecture:
            spec.architecture = spec.root.architecture
        else:
            spec.architecture = spack.architecture.sys_type()

        assert(spec.architecture is not None)
        return True   # changed


    def concretize_variants(self, spec):
        """If the spec already has variants filled in, return.  Otherwise, add
           the default variants from the package specification.
        """
        changed = False
        for name, variant in spec.package_class.variants.items():
            if name not in spec.variants:
                spec.variants[name] = spack.spec.VariantSpec(name, variant.default)
                changed = True
        return changed


    def concretize_compiler(self, spec):
        """If the spec already has a compiler, we're done.  If not, then take
           the compiler used for the nearest ancestor with a compiler
           spec and use that.  If the ancestor's compiler is not
           concrete, then used the preferred compiler as specified in
           spackconfig.

           Intuition: Use the spackconfig default if no package that depends on
           this one has a strict compiler requirement.  Otherwise, try to
           build with the compiler that will be used by libraries that
           link to this one, to maximize compatibility.
        """
        all_compilers = spack.compilers.all_compilers()

        if (spec.compiler and
            spec.compiler.concrete and
            spec.compiler in all_compilers):
            return False

        #Find the another spec that has a compiler, or the root if none do
        other_spec = spec if spec.compiler else find_spec(spec, lambda(x) : x.compiler)
        if not other_spec:
            other_spec = spec.root
        other_compiler = other_spec.compiler
        assert(other_spec)

        # Check if the compiler is already fully specified
        if other_compiler in all_compilers:
            spec.compiler = other_compiler.copy()
            return True

        # Filter the compilers into a sorted list based on the compiler_order from spackconfig
        compiler_list = all_compilers if not other_compiler else spack.compilers.find(other_compiler)
        cmp_compilers = partial(spack.pkgsort.compiler_compare, other_spec.name)
        matches = sorted(compiler_list, cmp=cmp_compilers)
        if not matches:
            raise UnavailableCompilerVersionError(other_compiler)

        # copy concrete version into other_compiler
        spec.compiler = matches[0].copy()
        assert(spec.compiler.concrete)
        return True  # things changed.


def find_spec(spec, condition):
    """Searches the dag from spec in an intelligent order and looks
       for a spec that matches a condition"""
    # First search parents, then search children
    dagiter = chain(spec.traverse(direction='parents',  root=False),
                    spec.traverse(direction='children', root=False))
    visited = set()
    for relative in dagiter:
        if condition(relative):
            return relative
        visited.add(id(relative))

    # Then search all other relatives in the DAG *except* spec
    for relative in spec.root.traverse():
        if relative is spec: continue
        if id(relative) in visited: continue
        if condition(relative):
            return relative

    # Finally search spec itself.
    if condition(spec):
        return spec

    return None   # Nothing matched the condition.


def cmp_specs(lhs, rhs):
    # Package name sort order is not configurable, always goes alphabetical
    if lhs.name != rhs.name:
        return cmp(lhs.name, rhs.name)

    # Package version is second in compare order
    pkgname = lhs.name
    if lhs.versions != rhs.versions:
        return spack.pkgsort.version_compare(
            pkgname, lhs.versions, rhs.versions)

    # Compiler is third
    if lhs.compiler != rhs.compiler:
        return spack.pkgsort.compiler_compare(
            pkgname, lhs.compiler, rhs.compiler)

    # Variants
    if lhs.variants != rhs.variants:
        return spack.pkgsort.variant_compare(
            pkgname, lhs.variants, rhs.variants)

    # Architecture
    if lhs.architecture != rhs.architecture:
        return spack.pkgsort.architecture_compare(
            pkgname, lhs.architecture, rhs.architecture)

    # Dependency is not configurable
    lhash, rhash = hash(lhs), hash(rhs)
    if lhash != rhash:
        return -1 if lhash < rhash else 1

    # Equal specs
    return 0



class UnavailableCompilerVersionError(spack.error.SpackError):
    """Raised when there is no available compiler that satisfies a
       compiler spec."""
    def __init__(self, compiler_spec):
        super(UnavailableCompilerVersionError, self).__init__(
            "No available compiler version matches '%s'" % compiler_spec,
            "Run 'spack compilers' to see available compiler Options.")


class NoValidVersionError(spack.error.SpackError):
    """Raised when there is no way to have a concrete version for a
       particular spec."""
    def __init__(self, spec):
        super(NoValidVersionError, self).__init__(
            "There are no valid versions for %s that match '%s'" % (spec.name, spec.versions))


class NoBuildError(spack.error.SpackError):
    """Raised when a package is configured with the buildable option False, but
       no satisfactory external versions can be found"""
    def __init__(self, spec):
        super(NoBuildError, self).__init__(
            "The spec '%s' is configured as not buildable, and no matching external installs were found" % spec.name)
