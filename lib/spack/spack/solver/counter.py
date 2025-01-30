# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
from typing import Dict, List, Optional, Set, Tuple

import spack.config
import spack.deptypes as dt
import spack.repo
import spack.spec

from .context import Context

PossibleDependencies = Set[str]


class Counter:
    """Computes the possible packages and the maximum number of duplicates
    allowed for each of them.

    Args:
        specs: abstract specs to concretize
        tests: if True, add test dependencies to the list of possible packages
    """

    def __init__(self, specs: List["spack.spec.Spec"], tests: bool) -> None:
        self.context = Context(configuration=spack.config.CONFIG)
        self.analyzer = PossibleDependenciesAnalyzer(self.context)
        self.specs = specs
        self.link_run_types: dt.DepFlag = dt.LINK | dt.RUN | dt.TEST
        self.all_types: dt.DepFlag = dt.ALL
        if not tests:
            self.link_run_types = dt.LINK | dt.RUN
            self.all_types = dt.LINK | dt.RUN | dt.BUILD

        self._possible_dependencies: PossibleDependencies = set()
        self._possible_virtuals: Set[str] = set(x.name for x in specs if x.virtual)

    def possible_dependencies(self) -> PossibleDependencies:
        """Returns the list of possible dependencies"""
        self.ensure_cache_values()
        return self._possible_dependencies

    def possible_virtuals(self) -> Set[str]:
        """Returns the list of possible virtuals"""
        self.ensure_cache_values()
        return self._possible_virtuals

    def ensure_cache_values(self) -> None:
        """Ensure the cache values have been computed"""
        if self._possible_dependencies:
            return
        self._compute_cache_values()

    def possible_packages_facts(self, gen: "spack.solver.asp.PyclingoDriver", fn) -> None:
        """Emit facts associated with the possible packages"""
        raise NotImplementedError("must be implemented by derived classes")

    def _compute_cache_values(self):
        raise NotImplementedError("must be implemented by derived classes")


class NoDuplicatesCounter(Counter):
    def _compute_cache_values(self):
        self._possible_dependencies, virtuals = self.analyzer.possible_dependencies(
            *self.specs, allowed_deps=self.all_types
        )
        self._possible_virtuals.update(virtuals)

    def possible_packages_facts(self, gen, fn):
        gen.h2("Maximum number of nodes (packages)")
        for package_name in sorted(self.possible_dependencies()):
            gen.fact(fn.max_dupes(package_name, 1))
        gen.newline()
        gen.h2("Maximum number of nodes (virtual packages)")
        for package_name in sorted(self.possible_virtuals()):
            gen.fact(fn.max_dupes(package_name, 1))
        gen.newline()
        gen.h2("Possible package in link-run subDAG")
        for name in sorted(self.possible_dependencies()):
            gen.fact(fn.possible_in_link_run(name))
        gen.newline()


class MinimalDuplicatesCounter(NoDuplicatesCounter):
    def __init__(self, specs, tests):
        super().__init__(specs, tests)
        self._link_run: PossibleDependencies = set()
        self._direct_build: PossibleDependencies = set()
        self._total_build: PossibleDependencies = set()
        self._link_run_virtuals: Set[str] = set()

    def _compute_cache_values(self):
        self._link_run, virtuals = self.analyzer.possible_dependencies(
            *self.specs, allowed_deps=self.link_run_types
        )
        self._possible_virtuals.update(virtuals)
        self._link_run_virtuals.update(virtuals)
        for x in self._link_run:
            reals, virtuals = self.analyzer.possible_dependencies(
                x, allowed_deps=dt.BUILD, transitive=False, strict_depflag=True
            )
            self._possible_virtuals.update(virtuals)
            self._direct_build.update(reals)

        self._total_build, virtuals = self.analyzer.possible_dependencies(
            *self._direct_build, allowed_deps=self.all_types
        )
        self._possible_virtuals.update(virtuals)
        self._possible_dependencies = set(self._link_run) | set(self._total_build)

    def possible_packages_facts(self, gen, fn):
        build_tools = spack.repo.PATH.packages_with_tags("build-tools")
        gen.h2("Packages with at most a single node")
        for package_name in sorted(self.possible_dependencies() - build_tools):
            gen.fact(fn.max_dupes(package_name, 1))
        gen.newline()

        gen.h2("Packages with at multiple possible nodes (build-tools)")
        for package_name in sorted(self.possible_dependencies() & build_tools):
            gen.fact(fn.max_dupes(package_name, 2))
            gen.fact(fn.multiple_unification_sets(package_name))
        gen.newline()

        gen.h2("Maximum number of nodes (virtual packages)")
        for package_name in sorted(self.possible_virtuals()):
            gen.fact(fn.max_dupes(package_name, 1))
        gen.newline()

        gen.h2("Possible package in link-run subDAG")
        for name in sorted(self._link_run):
            gen.fact(fn.possible_in_link_run(name))
        gen.newline()


class FullDuplicatesCounter(MinimalDuplicatesCounter):
    def possible_packages_facts(self, gen, fn):
        build_tools = spack.repo.PATH.packages_with_tags("build-tools")
        counter = collections.Counter(
            list(self._link_run) + list(self._total_build) + list(self._direct_build)
        )
        gen.h2("Maximum number of nodes")
        for pkg, count in sorted(counter.items(), key=lambda x: (x[1], x[0])):
            count = min(count, 2)
            gen.fact(fn.max_dupes(pkg, count))
        gen.newline()

        gen.h2("Build unification sets ")
        for name in sorted(self.possible_dependencies() & build_tools):
            gen.fact(fn.multiple_unification_sets(name))
        gen.newline()

        gen.h2("Possible package in link-run subDAG")
        for name in sorted(self._link_run):
            gen.fact(fn.possible_in_link_run(name))
        gen.newline()

        counter = collections.Counter(
            list(self._link_run_virtuals) + list(self._possible_virtuals)
        )
        gen.h2("Maximum number of virtual nodes")
        for pkg, count in sorted(counter.items(), key=lambda x: (x[1], x[0])):
            gen.fact(fn.max_dupes(pkg, count))
        gen.newline()


class PossibleDependenciesAnalyzer:
    @staticmethod
    def from_config(configuration: spack.config.Configuration) -> "PossibleDependenciesAnalyzer":
        return PossibleDependenciesAnalyzer(Context(configuration=configuration))

    def __init__(self, context: Context) -> None:
        self.context = context
        self.runtime_pkgs, self.runtime_virtuals = self.context.runtime_pkgs()

    def possible_dependencies(
        self,
        *specs: spack.spec.Spec,
        allowed_deps: dt.DepFlag,
        transitive: bool = True,
        strict_depflag: bool = False,
    ) -> Tuple[Set[str], Set[str]]:
        virtuals: Set[str] = set()
        packages = []
        for current_spec in specs:
            if isinstance(current_spec, str):
                current_spec = spack.spec.Spec(current_spec)

            if self.context.repo.is_virtual(current_spec.name):
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
                transitive=transitive,
                expand_virtuals=True,
                depflag=allowed_deps,
                virtuals=virtuals,
                strict_depflag=strict_depflag,
            )

        virtuals.update(self.runtime_virtuals)
        real_packages = set(visited) | self.runtime_pkgs
        return real_packages, virtuals

    def _possible_dependencies(
        self,
        pkg_cls,
        *,
        transitive: bool,
        expand_virtuals: bool = True,
        depflag: dt.DepFlag,
        strict_depflag: bool = False,
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

        # At the moment exit early. Since libc is not buildable, there is no
        # need to extend the search space with libc dependencies.
        if pkg_cls.name in self.context.libc_pkgs():
            return visited

        for name, conditions in pkg_cls.dependencies_by_name(when=True).items():
            if all(
                self.context.unreachable(pkg_name=pkg_cls.name, when_spec=x) for x in conditions
            ):
                # print(
                #     f"Not adding {name} as a dep of {pkg_cls.name}, "
                #     f"because conditions cannot be met"
                # )
                continue

            # check whether this dependency could be of the type asked for
            if strict_depflag is False:
                depflag_union = 0
                for deplist in conditions.values():
                    for dep in deplist:
                        depflag_union |= dep.depflag
                if not (depflag & depflag_union):
                    continue
            else:
                if all(
                    dep.depflag != depflag for deplist in conditions.values() for dep in deplist
                ):
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
