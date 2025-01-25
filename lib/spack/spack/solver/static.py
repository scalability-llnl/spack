# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Static analysis to optimize input creation for clingo"""
from typing import Dict, List, Optional, Set, Tuple

import archspec.cpu

from llnl.util import lang

import spack.config
import spack.deptypes as dt
import spack.platforms
import spack.repo
import spack.spec
import spack.store

RUNTIME_TAG = "runtime"


class Context:
    """A full Spack context that can be passed around as an object"""

    def __init__(self, *, configuration: spack.config.Configuration):
        self.configuration = configuration
        self.repo = spack.repo.create(configuration)
        self.store = spack.store.create(configuration)

    def runtime_pkgs(self) -> Tuple[Set[str], Set[str]]:
        """Returns the runtime packages for this context, and the virtuals they may provide"""
        runtime_pkgs = set(self.repo.packages_with_tags(RUNTIME_TAG))
        runtime_virtuals = set()
        for x in runtime_pkgs:
            pkg_class = self.repo.get_pkg_class(x)
            runtime_virtuals.update(pkg_class.provided_virtual_names())
        return runtime_pkgs, runtime_virtuals

    def is_virtual(self, name: str) -> bool:
        return self.repo.is_virtual(name)

    @lang.memoized
    def providers_for(self, virtual_str: str) -> List[spack.spec.Spec]:
        candidates = self.repo.providers_for(virtual_str)
        result = []
        for spec in candidates:
            if not self._is_provider_candidate(pkg_name=spec.name, virtual=virtual_str):
                continue
            result.append(spec)
        return result

    @lang.memoized
    def is_allowed_on_this_platform(self, *, pkg_name: str) -> bool:
        # Check the package recipe
        pkg_cls = self.repo.get_pkg_class(pkg_name)
        platform_condition = (
            f"platform={spack.platforms.host()} target={archspec.cpu.host().family}:"
        )
        for when_spec, conditions in pkg_cls.requirements.items():
            if not when_spec.intersects(platform_condition):
                continue
            for requirements, _, _ in conditions:
                if not any(x.intersects(platform_condition) for x in requirements):
                    print(f"{pkg_name} is not for this platform")
                    return False

        return True

    @lang.memoized
    def can_be_installed(self, *, pkg_name) -> bool:
        if self.configuration.get(f"packages:{pkg_name}:buildable", True):
            return True

        if self.configuration.get(f"packages:{pkg_name}:externals", []):
            return True

        if self.store.db.query(pkg_name):
            return True

        # TODO: query buildcaches
        print(f"{pkg_name} cannot be installed")
        return False

    @lang.memoized
    def _is_provider_candidate(self, *, pkg_name: str, virtual: str) -> bool:
        if self.configuration.get("concretizer:preferred_providers_only", False):
            virtual_spec = spack.spec.Spec(virtual)
            preferred_providers = self.configuration.get(
                f"packages:all:providers:{virtual_spec.name}"
            )
            preferred_providers = [spack.spec.Spec(x) for x in preferred_providers]
            if not any(x.intersects(pkg_name) for x in preferred_providers):
                print(f"{pkg_name} is not among preferred providers for {virtual}")
                return False

        if not self.is_allowed_on_this_platform(pkg_name=pkg_name):
            return False

        if not self.can_be_installed(pkg_name=pkg_name):
            return False

        return True


class PossibleDependenciesAnalyzer:
    @staticmethod
    def from_config(configuration: spack.config.Configuration) -> "PossibleDependenciesAnalyzer":
        return PossibleDependenciesAnalyzer(Context(configuration=configuration))

    def __init__(self, context: Context):
        self.context = context
        self.runtime_pkgs, self.runtime_virtuals = self.context.runtime_pkgs()

    def possible_dependencies(
        self, *specs: spack.spec.Spec, allowed_deps: dt.DepFlag
    ) -> Tuple[Set[str], Set[str]]:
        virtuals: Set[str] = set()

        packages = []
        for current_spec in specs:
            if isinstance(current_spec, str):
                current_spec = spack.spec.Spec(current_spec)

            if spack.repo.PATH.is_virtual(current_spec.name):
                packages.extend(
                    [
                        (current_spec, p.package_class)
                        for p in self.context.providers_for(current_spec.name)
                    ]
                )
                continue
            packages.append((current_spec, current_spec.package_class))

        visited: Dict[str, Set[str]] = {}
        for input_spec, pkg_cls in packages:
            self._possible_dependencies(
                pkg_cls,
                visited=visited,
                transitive=True,
                expand_virtuals=True,
                depflag=allowed_deps,
                virtuals=virtuals,
            )

        virtuals.update(self.runtime_virtuals)
        real_packages = set(visited) | self.runtime_pkgs
        return real_packages, virtuals

    def _possible_dependencies(
        self,
        pkg_cls,
        *,
        transitive: bool = True,
        expand_virtuals: bool = True,
        depflag: dt.DepFlag = dt.ALL,
        visited: Optional[dict] = None,
        missing: Optional[dict] = None,
        virtuals: set,
    ) -> Dict[str, Set[str]]:
        """Return dict of possible dependencies of this package.

        Args:
            transitive (bool or None): return all transitive dependencies if
                True, only direct dependencies if False (default True)..
            expand_virtuals (bool or None): expand virtual dependencies into
                all possible implementations (default True)
            depflag: dependency types to consider
            visited (dict or None): dict of names of dependencies visited so
                far, mapped to their immediate dependencies' names.
            missing (dict or None): dict to populate with packages and their
                *missing* dependencies.
            virtuals (set): if provided, populate with virtuals seen so far.

        Returns:
            (dict): dictionary mapping dependency names to *their*
                immediate dependencies

        Each item in the returned dictionary maps a (potentially
        transitive) dependency of this package to its possible
        *immediate* dependencies. If ``expand_virtuals`` is ``False``,
        virtual package names wil be inserted as keys mapped to empty
        sets of dependencies.  Virtuals, if not expanded, are treated as
        though they have no immediate dependencies.

        Missing dependencies by default are ignored, but if a
        missing dict is provided, it will be populated with package names
        mapped to any dependencies they have that are in no
        repositories. This is only populated if transitive is True.

        Note: the returned dict *includes* the package itself.

        """
        visited = {} if visited is None else visited
        missing = {} if missing is None else missing

        visited.setdefault(pkg_cls.name, set())

        for name, conditions in pkg_cls.dependencies_by_name(when=True).items():
            # check whether this dependency could be of the type asked for
            depflag_union = 0
            for deplist in conditions.values():
                for dep in deplist:
                    depflag_union |= dep.depflag
            if not (depflag & depflag_union):
                continue

            if self.context.is_virtual(name) and name in virtuals:
                continue

            # expand virtuals if enabled, otherwise just stop at virtuals
            if self.context.is_virtual(name):
                virtuals.add(name)
                if expand_virtuals:
                    providers = self.context.providers_for(name)
                    dep_names = {spec.name for spec in providers}
                else:
                    visited.setdefault(pkg_cls.name, set()).add(name)
                    visited.setdefault(name, set())
                    continue
            else:
                dep_names = {name}

            # add the dependency names to the visited dict
            visited.setdefault(pkg_cls.name, set()).update(dep_names)

            # recursively traverse dependencies
            for dep_name in dep_names:
                if dep_name in visited:
                    continue

                visited.setdefault(dep_name, set())

                if not self.context.is_allowed_on_this_platform(pkg_name=dep_name):
                    continue

                if not self.context.can_be_installed(pkg_name=dep_name):
                    continue

                # skip the rest if not transitive
                if not transitive:
                    continue

                try:
                    dep_cls = self.context.repo.get_pkg_class(dep_name)
                except spack.repo.UnknownPackageError:
                    # log unknown packages
                    missing.setdefault(pkg_cls.name, set()).add(dep_name)
                    continue

                self._possible_dependencies(
                    dep_cls,
                    transitive=transitive,
                    expand_virtuals=expand_virtuals,
                    depflag=depflag,
                    visited=visited,
                    missing=missing,
                    virtuals=virtuals,
                )

        return visited
