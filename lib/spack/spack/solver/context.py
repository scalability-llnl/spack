# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Dict, List, NamedTuple, Set, Tuple, Union

import archspec.cpu

from llnl.util import lang, tty

import spack.binary_distribution
import spack.config
import spack.deptypes as dt
import spack.platforms
import spack.repo
import spack.spec
import spack.store
from spack.error import SpackError

RUNTIME_TAG = "runtime"


class Context(NamedTuple):
    configuration: spack.config.Configuration
    repo: spack.repo.RepoPath
    store: spack.store.Store
    binary_index: spack.binary_distribution.BinaryCacheIndex


class PossibleGraph(NamedTuple):
    real_pkgs: Set[str]
    virtuals: Set[str]
    edges: Dict[str, Set[str]]


class PossibleDependencyGraph:
    """Returns information needed to set up an ASP problem"""

    def unreachable(self, *, pkg_name: str, when_spec: spack.spec.Spec) -> bool:
        """Returns true if the context can determine that the condition cannot ever
        be met on pkg_name.
        """
        raise NotImplementedError

    def candidate_targets(self) -> List[archspec.cpu.Microarchitecture]:
        """Returns a list of targets that are candidate for concretization"""
        raise NotImplementedError

    def possible_dependencies(
        self,
        *specs: Union[spack.spec.Spec, str],
        allowed_deps: dt.DepFlag,
        transitive: bool = True,
        strict_depflag: bool = False,
        expand_virtuals: bool = True,
    ) -> PossibleGraph:
        """Returns the set of possible dependencies, and the set of possible virtuals.

        Both sets always include runtime packages, which may be injected by compilers.

        Args:
            transitive: return transitive dependencies if True, only direct dependencies if False
            allowed_deps: dependency types to consider
            strict_depflag: if True, only the specific dep type is considered, if False any
                deptype that intersects with allowed deptype is considered
            expand_virtuals: expand virtual dependencies into all possible implementations
        """
        raise NotImplementedError


class NoStaticAnalysis(PossibleDependencyGraph):
    """Implementation that tries to minimize the setup time (i.e. defaults to give fast
    answers), rather than trying to reduce the ASP problem size with more complex analysis.
    """

    def __init__(self, *, context: Context):
        self.context = context
        self.runtime_pkgs = set(self.context.repo.packages_with_tags(RUNTIME_TAG))
        self.runtime_virtuals = set()
        for x in self.runtime_pkgs:
            pkg_class = self.context.repo.get_pkg_class(x)
            self.runtime_virtuals.update(pkg_class.provided_virtual_names())

        try:
            self.libc_pkgs = [x.name for x in self.providers_for("libc")]
        except spack.repo.UnknownPackageError:
            self.libc_pkgs = []

    @property
    def configuration(self):
        return self.context.configuration

    @property
    def repo(self):
        return self.context.repo

    @property
    def store(self):
        return self.context.store

    @lang.memoized
    def buildcache_specs(self) -> List[spack.spec.Spec]:
        self.context.binary_index.update()
        return self.context.binary_index.get_all_built_specs()

    def is_virtual(self, name: str) -> bool:
        return self.context.repo.is_virtual(name)

    @lang.memoized
    def is_allowed_on_this_platform(self, *, pkg_name: str) -> bool:
        """Returns true if a package is allowed on the current host"""
        pkg_cls = self.context.repo.get_pkg_class(pkg_name)
        platform_condition = (
            f"platform={spack.platforms.host()} target={archspec.cpu.host().family}:"
        )
        for when_spec, conditions in pkg_cls.requirements.items():
            if not when_spec.intersects(platform_condition):
                continue
            for requirements, _, _ in conditions:
                if not any(x.intersects(platform_condition) for x in requirements):
                    tty.debug(f"[{__name__}] {pkg_name} is not for this platform")
                    return False
        return True

    def providers_for(self, virtual_str: str) -> List[spack.spec.Spec]:
        """Returns a list of possible providers for the virtual string in input."""
        return self.context.repo.providers_for(virtual_str)

    def can_be_installed(self, *, pkg_name) -> bool:
        """Returns True if a package can be installed, False otherwise."""
        return True

    def unreachable(self, *, pkg_name: str, when_spec: spack.spec.Spec) -> bool:
        """Returns true if the context can determine that the condition cannot ever
        be met on pkg_name.
        """
        return False

    def candidate_targets(self) -> List[archspec.cpu.Microarchitecture]:
        """Returns a list of targets that are candidate for concretization"""
        platform = spack.platforms.host()
        default_target = archspec.cpu.TARGETS[platform.default]

        # Construct the list of targets which are compatible with the host
        candidate_targets = [default_target] + default_target.ancestors
        granularity = self.context.configuration.get("concretizer:targets:granularity")
        host_compatible = self.context.configuration.get("concretizer:targets:host_compatible")

        # Add targets which are not compatible with the current host
        if not host_compatible:
            additional_targets_in_family = sorted(
                [
                    t
                    for t in archspec.cpu.TARGETS.values()
                    if (t.family.name == default_target.family.name and t not in candidate_targets)
                ],
                key=lambda x: len(x.ancestors),
                reverse=True,
            )
            candidate_targets += additional_targets_in_family

        # Check if we want only generic architecture
        if granularity == "generic":
            candidate_targets = [t for t in candidate_targets if t.vendor == "generic"]

        return candidate_targets

    def possible_dependencies(
        self,
        *specs: Union[spack.spec.Spec, str],
        allowed_deps: dt.DepFlag,
        transitive: bool = True,
        strict_depflag: bool = False,
        expand_virtuals: bool = True,
    ) -> PossibleGraph:
        stack = [x for x in self._package_list(specs)]
        virtuals: Set[str] = set()
        edges: Dict[str, Set[str]] = {}

        while stack:
            pkg_name = stack.pop()

            if pkg_name in edges:
                continue

            edges[pkg_name] = set()

            # Since libc is not buildable, there is no need to extend the
            # search space with libc dependencies.
            if pkg_name in self.libc_pkgs:
                continue

            pkg_cls = self.context.repo.get_pkg_class(pkg_name=pkg_name)
            for name, conditions in pkg_cls.dependencies_by_name(when=True).items():
                if all(self.unreachable(pkg_name=pkg_name, when_spec=x) for x in conditions):
                    tty.debug(
                        f"[{__name__}] Not adding {name} as a dep of {pkg_name}, because "
                        f"conditions cannot be met"
                    )
                    continue

                if not self._has_deptypes(
                    conditions, allowed_deps=allowed_deps, strict=strict_depflag
                ):
                    continue

                if name in virtuals:
                    continue

                dep_names = set()
                if self.is_virtual(name):
                    virtuals.add(name)
                    if expand_virtuals:
                        providers = self.providers_for(name)
                        dep_names = {spec.name for spec in providers}
                else:
                    dep_names = {name}

                edges[pkg_name].update(dep_names)

                if not transitive:
                    continue

                for dep_name in dep_names:
                    if dep_name in edges:
                        continue

                    if not self._is_possible(pkg_name=dep_name):
                        continue

                    stack.append(dep_name)

        real_packages = set(edges)
        if not transitive:
            # We exit early, so add children from the edges information
            for root, children in edges.items():
                real_packages.update(x for x in children if self._is_possible(pkg_name=x))

        virtuals.update(self.runtime_virtuals)
        real_packages = real_packages | self.runtime_pkgs
        return PossibleGraph(real_pkgs=real_packages, virtuals=virtuals, edges=edges)

    def _package_list(self, specs: Tuple[Union[spack.spec.Spec, str], ...]) -> List[str]:
        stack = []
        for current_spec in specs:
            if isinstance(current_spec, str):
                current_spec = spack.spec.Spec(current_spec)

            if self.context.repo.is_virtual(current_spec.name):
                stack.extend([p.name for p in self.providers_for(current_spec.name)])
                continue

            stack.append(current_spec.name)
        return sorted(set(stack))

    def _has_deptypes(self, dependencies, *, allowed_deps: dt.DepFlag, strict: bool) -> bool:
        if strict is True:
            return any(
                dep.depflag == allowed_deps for deplist in dependencies.values() for dep in deplist
            )
        return any(
            dep.depflag & allowed_deps for deplist in dependencies.values() for dep in deplist
        )

    def _is_possible(self, *, pkg_name):
        try:
            return self.is_allowed_on_this_platform(pkg_name=pkg_name) and self.can_be_installed(
                pkg_name=pkg_name
            )
        except spack.repo.UnknownPackageError:
            return False


class StaticAnalysis(NoStaticAnalysis):
    """Performs some static analysis of the configuration, store, etc. to provide more precise
    answers on whether some packages can be installed, or used as a provider.

    It increases the setup time, but might decrease the grounding and solve time considerably,
    especially when requirements restrict the possible choices for providers.
    """

    @lang.memoized
    def providers_for(self, virtual_str: str) -> List[spack.spec.Spec]:
        candidates = super().providers_for(virtual_str)
        result = []
        for spec in candidates:
            if not self._is_provider_candidate(pkg_name=spec.name, virtual=virtual_str):
                continue
            result.append(spec)
        return result

    @lang.memoized
    def can_be_installed(self, *, pkg_name) -> bool:
        if self.context.configuration.get(f"packages:{pkg_name}:buildable", True):
            return True

        if self.context.configuration.get(f"packages:{pkg_name}:externals", []):
            return True

        reuse = self.context.configuration.get("concretizer:reuse")
        if reuse is not False and self.store.db.query(pkg_name):
            return True

        if reuse is not False and any(x.name == pkg_name for x in self.buildcache_specs()):
            return True

        tty.debug(f"[{__name__}] {pkg_name} cannot be installed")
        return False

    @lang.memoized
    def _is_provider_candidate(self, *, pkg_name: str, virtual: str) -> bool:
        if not self.is_allowed_on_this_platform(pkg_name=pkg_name):
            return False

        if not self.can_be_installed(pkg_name=pkg_name):
            return False

        virtual_spec = spack.spec.Spec(virtual)
        if self.unreachable(pkg_name=virtual_spec.name, when_spec=pkg_name):
            tty.debug(f"[{__name__}] {pkg_name} cannot be a provider for {virtual}")
            return False

        return True

    @lang.memoized
    def unreachable(self, *, pkg_name: str, when_spec: spack.spec.Spec) -> bool:
        """Returns true if the context can determine that the condition cannot ever
        be met on pkg_name.
        """
        candidates = self.context.configuration.get(f"packages:{pkg_name}:require", [])
        if not candidates and pkg_name != "all":
            return self.unreachable(pkg_name="all", when_spec=when_spec)

        if not candidates:
            return False

        if isinstance(candidates, str):
            candidates = [candidates]

        union_requirement = spack.spec.Spec()
        for c in candidates:
            if not isinstance(c, str):
                continue
            try:
                union_requirement.constrain(c)
            except SpackError:
                # Less optimized, but shouldn't fail
                pass

        if not union_requirement.intersects(when_spec):
            return True

        return False


def create_inspector(context: Context) -> PossibleDependencyGraph:
    static_analysis = context.configuration.get("concretizer:static_analysis", False)
    if static_analysis:
        return StaticAnalysis(context=context)
    return NoStaticAnalysis(context=context)


def default_context() -> Context:
    return Context(
        configuration=spack.config.CONFIG,
        repo=spack.repo.PATH,
        store=spack.store.STORE,
        binary_index=spack.binary_distribution.BINARY_INDEX,
    )


def default_inspector() -> PossibleDependencyGraph:
    return create_inspector(default_context())
