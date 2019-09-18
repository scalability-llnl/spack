# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
from __future__ import print_function

import os.path
import tempfile
import llnl.util.filesystem as fs
import llnl.util.tty as tty

from itertools import chain
from functools_backport import reverse_order
from contextlib import contextmanager
from six import iteritems

import llnl.util.lang

import spack.repo
import spack.abi
import spack.spec
import spack.compilers
import spack.architecture
import spack.error
import spack.tengine
from spack.config import config
from spack.version import ver, Version, VersionList, VersionRange
from spack.package_prefs import PackagePrefs, spec_externals, is_spec_buildable


#: Concretizer singleton
concretizer = llnl.util.lang.Singleton(lambda: Concretizer())


#: impements rudimentary logic for ABI compatibility
_abi = llnl.util.lang.Singleton(lambda: spack.abi.ABI())


class Concretizer(object):
    """You can subclass this class to override some of the default
       concretization strategies, or you can override all of them.
    """
    def __init__(self):
        # controls whether we check that compiler versions actually exist
        # during concretization. Used for testing and for mirror creation
        self.check_for_compiler_existence = not config.get(
            'config:install_missing_compilers', False)

    @contextmanager
    def disable_compiler_existence_check(self):
        saved = self.check_for_compiler_existence
        self.check_for_compiler_existence = False
        yield
        self.check_for_compiler_existence = saved

    @contextmanager
    def enable_compiler_existence_check(self):
        saved = self.check_for_compiler_existence
        self.check_for_compiler_existence = True
        yield
        self.check_for_compiler_existence = saved

    def _valid_virtuals_and_externals(self, spec):
        """Returns a list of candidate virtual dep providers and external
           packages that coiuld be used to concretize a spec.

           Preferred specs come first in the list.
        """
        # First construct a list of concrete candidates to replace spec with.
        candidates = [spec]
        pref_key = lambda spec: 0  # no-op pref key

        if spec.virtual:
            candidates = spack.repo.path.providers_for(spec)
            if not candidates:
                raise spack.spec.UnsatisfiableProviderSpecError(
                    candidates[0], spec)

            # Find nearest spec in the DAG (up then down) that has prefs.
            spec_w_prefs = find_spec(
                spec, lambda p: PackagePrefs.has_preferred_providers(
                    p.name, spec.name),
                spec)  # default to spec itself.

            # Create a key to sort candidates by the prefs we found
            pref_key = PackagePrefs(spec_w_prefs.name, 'providers', spec.name)

        # For each candidate package, if it has externals, add those
        # to the usable list.  if it's not buildable, then *only* add
        # the externals.
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

        # Use a sort key to order the results
        return sorted(usable, key=lambda spec: (
            not spec.external,                            # prefer externals
            pref_key(spec),                               # respect prefs
            spec.name,                                    # group by name
            reverse_order(spec.versions),                 # latest version
            spec                                          # natural order
        ))

    def choose_virtual_or_external(self, spec):
        """Given a list of candidate virtual and external packages, try to
           find one that is most ABI compatible.
        """
        candidates = self._valid_virtuals_and_externals(spec)
        if not candidates:
            return candidates

        # Find the nearest spec in the dag that has a compiler.  We'll
        # use that spec to calibrate compiler compatibility.
        abi_exemplar = find_spec(spec, lambda x: x.compiler)
        if abi_exemplar is None:
            abi_exemplar = spec.root

        # Sort candidates from most to least compatibility.
        #   We reverse because True > False.
        #   Sort is stable, so candidates keep their order.
        return sorted(candidates,
                      reverse=True,
                      key=lambda spec: (
                          _abi.compatible(spec, abi_exemplar, loose=True),
                          _abi.compatible(spec, abi_exemplar)))

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

        # List of versions we could consider, in sorted order
        pkg_versions = spec.package_class.versions
        usable = [v for v in pkg_versions
                  if any(v.satisfies(sv) for sv in spec.versions)]

        yaml_prefs = PackagePrefs(spec.name, 'version')

        # The keys below show the order of precedence of factors used
        # to select a version when concretizing.  The item with
        # the "largest" key will be selected.
        #
        # NOTE: When COMPARING VERSIONS, the '@develop' version is always
        #       larger than other versions.  BUT when CONCRETIZING,
        #       the largest NON-develop version is selected by default.
        keyfn = lambda v: (
            # ------- Special direction from the user
            # Respect order listed in packages.yaml
            -yaml_prefs(v),

            # The preferred=True flag (packages or packages.yaml or both?)
            pkg_versions.get(Version(v)).get('preferred', False),

            # ------- Regular case: use latest non-develop version by default.
            # Avoid @develop version, which would otherwise be the "largest"
            # in straight version comparisons
            not v.isdevelop(),

            # Compare the version itself
            # This includes the logic:
            #    a) develop > everything (disabled by "not v.isdevelop() above)
            #    b) numeric > non-numeric
            #    c) Numeric or string comparison
            v)
        usable.sort(key=keyfn, reverse=True)

        if usable:
            spec.versions = ver([usable[0]])
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
        """If the spec is empty provide the defaults of the platform. If the
        architecture is not a string type, then check if either the platform,
        target or operating system are concretized. If any of the fields are
        changed then return True. If everything is concretized (i.e the
        architecture attribute is a namedtuple of classes) then return False.
        If the target is a string type, then convert the string into a
        concretized architecture. If it has no architecture and the root of the
        DAG has an architecture, then use the root otherwise use the defaults
        on the platform.
        """
        try:
            # Get the nearest architecture with any fields set
            nearest = next(p for p in spec.traverse(direction='parents')
                           if (p.architecture and p is not spec))
            nearest_arch = nearest.architecture
        except StopIteration:
            # Default to the system architecture if nothing set
            nearest_arch = spack.spec.ArchSpec(spack.architecture.sys_type())

        spec_changed = False

        # ensure type safety for the architecture
        if spec.architecture is None:
            spec.architecture = spack.spec.ArchSpec()
            spec_changed = True

        # replace each of the fields (platform, os, target) separately
        nearest_dict = nearest_arch.to_cmp_dict()
        replacement_fields = [k for k, v in iteritems(nearest_dict)
                              if v and not getattr(spec.architecture, k)]
        for field in replacement_fields:
            setattr(spec.architecture, field, getattr(nearest_arch, field))
            spec_changed = True

        return spec_changed

    def concretize_variants(self, spec):
        """If the spec already has variants filled in, return.  Otherwise, add
           the user preferences from packages.yaml or the default variants from
           the package specification.
        """
        changed = False
        preferred_variants = PackagePrefs.preferred_variants(spec.name)
        pkg_cls = spec.package_class
        for name, variant in pkg_cls.variants.items():
            if name not in spec.variants:
                changed = True
                if name in preferred_variants:
                    spec.variants[name] = preferred_variants.get(name)
                else:
                    spec.variants[name] = variant.make_default()

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
        # Pass on concretizing the compiler if the target or operating system
        # is not yet determined
        if not (spec.architecture.os and spec.architecture.target):
            # We haven't changed, but other changes need to happen before we
            # continue. `return True` here to force concretization to keep
            # running.
            return True

        # Only use a matching compiler if it is of the proper style
        # Takes advantage of the proper logic already existing in
        # compiler_for_spec Should think whether this can be more
        # efficient
        def _proper_compiler_style(cspec, aspec):
            return spack.compilers.compilers_for_spec(cspec, arch_spec=aspec)

        if spec.compiler and spec.compiler.concrete:
            if (self.check_for_compiler_existence and not
                    _proper_compiler_style(spec.compiler, spec.architecture)):
                _compiler_concretization_failure(
                    spec.compiler, spec.architecture)
            return False

        # Find another spec that has a compiler, or the root if none do
        try:
            other_spec = spec if spec.compiler else next(
                p for p in spec.traverse(direction='parents') if p.compiler)
        except StopIteration:
            other_spec = spec.root

        other_compiler = other_spec.compiler
        assert(other_spec)

        def fetch_compiler_prefs(spec, other_spec, compiler_list):
            if not other_spec:
                # Only fall back to 'all' preferences if looking at other specs
                other_spec = spec
                if not PackagePrefs.has_preferred_compiler(spec.name):
                    return False

            # By default, prefer later versions of compilers
            compiler_list = sorted(
                compiler_list, key=lambda x: (x.name, x.version), reverse=True)
            ppk = PackagePrefs(other_spec.name, 'compiler')
            matches = sorted(compiler_list, key=ppk)

            # copy concrete version into other_compiler
            try:
                spec.compiler = next(
                    c for c in matches
                    if _proper_compiler_style(c, spec.architecture)).copy()
            except StopIteration:
                # No compiler with a satisfactory spec has a suitable arch
                _compiler_concretization_failure(
                    other_compiler, spec.architecture)

            assert(spec.compiler.concrete)
            return True

        if not spec.compiler and not other_compiler:
            # Only use compiler preferences if compiler has not been overriden
            compiler_list = spack.compilers.all_compiler_specs()
            if not compiler_list:
                # Spack has no compilers.
                raise spack.compilers.NoCompilersError()
            if fetch_compiler_prefs(spec, None, compiler_list):
                return True

        # Check if the compiler is already fully specified
        if other_compiler and other_compiler.concrete:
            if (self.check_for_compiler_existence and not
                    _proper_compiler_style(other_compiler, spec.architecture)):
                _compiler_concretization_failure(
                    other_compiler, spec.architecture)
            spec.compiler = other_compiler
            return True

        if other_compiler:  # Another node has abstract compiler information
            compiler_list = spack.compilers.find_specs_by_arch(
                other_compiler, spec.architecture
            )
            if not compiler_list:
                # We don't have a matching compiler installed
                if not self.check_for_compiler_existence:
                    # Concretize compiler spec versions as a package to build
                    cpkg_spec = spack.compilers.pkg_spec_for_compiler(
                        other_compiler
                    )
                    self.concretize_version(cpkg_spec)
                    spec.compiler = spack.spec.CompilerSpec(
                        other_compiler.name, cpkg_spec.versions)
                    return True
                else:
                    # No compiler with a satisfactory spec was found
                    raise UnavailableCompilerVersionError(other_compiler)
        else:
            # We have no hints to go by, grab any compiler
            compiler_list = spack.compilers.all_compiler_specs()
            if not compiler_list:
                # Spack has no compilers.
                raise spack.compilers.NoCompilersError()

        fetch_compiler_prefs(spec, other_spec, compiler_list)
        return True  # things changed.

    def concretize_compiler_flags(self, spec):
        """
        The compiler flags are updated to match those of the spec whose
        compiler is used, defaulting to no compiler flags in the spec.
        Default specs set at the compiler level will still be added later.
        """
        # Pass on concretizing the compiler flags if the target or operating
        # system is not set.
        if not (spec.architecture.os and spec.architecture.target):
            # We haven't changed, but other changes need to happen before we
            # continue. `return True` here to force concretization to keep
            # running.
            return True

        compiler_match = lambda other: (
            spec.compiler == other.compiler and
            spec.architecture == other.architecture)

        ret = False
        for flag in spack.spec.FlagMap.valid_compiler_flags():
            if flag not in spec.compiler_flags:
                spec.compiler_flags[flag] = list()
            try:
                nearest = next(p for p in spec.traverse(direction='parents')
                               if (compiler_match(p) and
                                   (p is not spec) and
                                   flag in p.compiler_flags))
                nearest_flags = nearest.compiler_flags.get(flag, [])
                flags = spec.compiler_flags.get(flag, [])
                if set(nearest_flags) - set(flags):
                    spec.compiler_flags[flag] = list(
                        llnl.util.lang.dedupe(nearest_flags + flags)
                    )
                    ret = True
            except StopIteration:
                pass

        # Include the compiler flag defaults from the config files
        # This ensures that spack will detect conflicts that stem from a change
        # in default compiler flags.
        try:
            compiler = spack.compilers.compiler_for_spec(
                spec.compiler, spec.architecture)
        except spack.compilers.NoCompilerForSpecError:
            if self.check_for_compiler_existence:
                raise
            return ret
        for flag in compiler.flags:
            config_flags = compiler.flags.get(flag, [])
            flags = spec.compiler_flags.get(flag, [])
            spec.compiler_flags[flag] = list(
                llnl.util.lang.dedupe(config_flags + flags)
            )
            if set(config_flags) - set(flags):
                ret = True

        return ret


def find_spec(spec, condition, default=None):
    """Searches the dag from spec in an intelligent order and looks
       for a spec that matches a condition"""
    # First search parents, then search children
    deptype = ('build', 'link')
    dagiter = chain(
        spec.traverse(direction='parents',  deptype=deptype, root=False),
        spec.traverse(direction='children', deptype=deptype, root=False))
    visited = set()
    for relative in dagiter:
        if condition(relative):
            return relative
        visited.add(id(relative))

    # Then search all other relatives in the DAG *except* spec
    for relative in spec.root.traverse(deptypes=all):
        if relative is spec:
            continue
        if id(relative) in visited:
            continue
        if condition(relative):
            return relative

    # Finally search spec itself.
    if condition(spec):
        return spec

    return default   # Nothing matched the condition; return default.


def _compiler_concretization_failure(compiler_spec, arch):
    # Distinguish between the case that there are compilers for
    # the arch but not with the given compiler spec and the case that
    # there are no compilers for the arch at all
    if not spack.compilers.compilers_for_arch(arch):
        available_os_targets = set(
            (c.operating_system, c.target) for c in
            spack.compilers.all_compilers())
        raise NoCompilersForArchError(arch, available_os_targets)
    else:
        raise UnavailableCompilerVersionError(compiler_spec, arch)


def concretize_specs_together(*abstract_specs):
    """Given a number of specs as input, tries to concretize them together.

    Args:
        *abstract_specs: abstract specs to be concretized, given either
            as Specs or strings

    Returns:
        List of concretized specs
    """
    def make_concretization_repository(abstract_specs):
        """Returns the path to a temporary repository created to contain
        a fake package that depends on all of the abstract specs.
        """
        tmpdir = tempfile.mkdtemp()
        repo_path, _ = spack.repo.create_repo(tmpdir)

        debug_msg = '[CONCRETIZATION]: Creating helper repository in {0}'
        tty.debug(debug_msg.format(repo_path))

        pkg_dir = os.path.join(repo_path, 'packages', 'concretizationroot')
        fs.mkdirp(pkg_dir)
        environment = spack.tengine.make_environment()
        template = environment.get_template('misc/coconcretization.pyt')

        # Split recursive specs, as it seems the concretizer has issue
        # respecting conditions on dependents expressed like
        # depends_on('foo ^bar@1.0'), see issue #11160
        split_specs = [dep.copy(deps=False)
                       for spec in abstract_specs
                       for dep in spec.traverse(root=True)]

        with open(os.path.join(pkg_dir, 'package.py'), 'w') as f:
            f.write(template.render(specs=[str(s) for s in split_specs]))

        return spack.repo.Repo(repo_path)

    abstract_specs = [spack.spec.Spec(s) for s in abstract_specs]
    concretization_repository = make_concretization_repository(abstract_specs)

    with spack.repo.additional_repository(concretization_repository):
        # Spec from a helper package that depends on all the abstract_specs
        concretization_root = spack.spec.Spec('concretizationroot')
        concretization_root.concretize()
        # Retrieve the direct dependencies
        concrete_specs = [
            concretization_root[spec.name].copy() for spec in abstract_specs
        ]

    return concrete_specs


class NoCompilersForArchError(spack.error.SpackError):
    def __init__(self, arch, available_os_targets):
        err_msg = ("No compilers found"
                   " for operating system %s and target %s."
                   "\nIf previous installations have succeeded, the"
                   " operating system may have been updated." %
                   (arch.os, arch.target))

        available_os_target_strs = list()
        for operating_system, t in available_os_targets:
            os_target_str = "%s-%s" % (operating_system, t) if t \
                else operating_system
            available_os_target_strs.append(os_target_str)
        err_msg += (
            "\nCompilers are defined for the following"
            " operating systems and targets:\n\t" +
            "\n\t".join(available_os_target_strs))

        super(NoCompilersForArchError, self).__init__(
            err_msg, "Run 'spack compiler find' to add compilers.")


class UnavailableCompilerVersionError(spack.error.SpackError):
    """Raised when there is no available compiler that satisfies a
       compiler spec."""

    def __init__(self, compiler_spec, arch=None):
        err_msg = "No compilers with spec {0} found".format(compiler_spec)
        if arch:
            err_msg += " for operating system {0} and target {1}.".format(
                arch.os, arch.target
            )

        super(UnavailableCompilerVersionError, self).__init__(
            err_msg, "Run 'spack compiler find' to add compilers.")


class NoValidVersionError(spack.error.SpackError):
    """Raised when there is no way to have a concrete version for a
       particular spec."""

    def __init__(self, spec):
        super(NoValidVersionError, self).__init__(
            "There are no valid versions for %s that match '%s'"
            % (spec.name, spec.versions))


class InsufficientArchitectureInfoError(spack.error.SpackError):

    """Raised when details on architecture cannot be collected from the
       system"""

    def __init__(self, spec, archs):
        super(InsufficientArchitectureInfoError, self).__init__(
            "Cannot determine necessary architecture information for '%s': %s"
            % (spec.name, str(archs)))


class NoBuildError(spack.error.SpackError):
    """Raised when a package is configured with the buildable option False, but
       no satisfactory external versions can be found"""

    def __init__(self, spec):
        msg = ("The spec\n    '%s'\n    is configured as not buildable, "
               "and no matching external installs were found")
        super(NoBuildError, self).__init__(msg % spec)
