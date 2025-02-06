# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
from typing import Dict, List, NamedTuple, Set, Tuple, Union

from llnl.util import tty

import spack.deptypes as dt
import spack.repo
import spack.spec

from .context import Context


class Counter:
    """Computes the possible packages and the maximum number of duplicates
    allowed for each of them.

    Args:
        specs: abstract specs to concretize
        tests: if True, add test dependencies to the list of possible packages
    """

    def __init__(self, specs: List["spack.spec.Spec"], tests: bool, context: Context) -> None:
        self.context = context
        self.analyzer = PossibleDependenciesAnalyzer(self.context)
        self.specs = specs
        self.link_run_types: dt.DepFlag = dt.LINK | dt.RUN | dt.TEST
        self.all_types: dt.DepFlag = dt.ALL
        if not tests:
            self.link_run_types = dt.LINK | dt.RUN
            self.all_types = dt.LINK | dt.RUN | dt.BUILD

        self._possible_dependencies: Set[str] = set()
        self._possible_virtuals: Set[str] = set(x.name for x in specs if x.virtual)

    def possible_dependencies(self) -> Set[str]:
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

    def possible_packages_facts(self, gen: "spack.solver.asp.ProblemInstanceBuilder", fn) -> None:
        """Emit facts associated with the possible packages"""
        raise NotImplementedError("must be implemented by derived classes")

    def _compute_cache_values(self) -> None:
        raise NotImplementedError("must be implemented by derived classes")


class NoDuplicatesCounter(Counter):
    def _compute_cache_values(self) -> None:
        self._possible_dependencies, virtuals, _ = self.analyzer.possible_dependencies(
            *self.specs, allowed_deps=self.all_types
        )
        self._possible_virtuals.update(virtuals)

    def possible_packages_facts(self, gen: "spack.solver.asp.ProblemInstanceBuilder", fn) -> None:
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
    def __init__(self, specs: List["spack.spec.Spec"], tests: bool, context: Context) -> None:
        super().__init__(specs, tests, context)
        self._link_run: Set[str] = set()
        self._direct_build: Set[str] = set()
        self._total_build: Set[str] = set()
        self._link_run_virtuals: Set[str] = set()

    def _compute_cache_values(self) -> None:
        self._link_run, virtuals, _ = self.analyzer.possible_dependencies(
            *self.specs, allowed_deps=self.link_run_types
        )
        self._possible_virtuals.update(virtuals)
        self._link_run_virtuals.update(virtuals)
        for x in self._link_run:
            reals, virtuals, _ = self.analyzer.possible_dependencies(
                x, allowed_deps=dt.BUILD, transitive=False, strict_depflag=True
            )
            self._possible_virtuals.update(virtuals)
            self._direct_build.update(reals)

        self._total_build, virtuals, _ = self.analyzer.possible_dependencies(
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


class PossibleGraph(NamedTuple):
    real_pkgs: Set[str]
    virtuals: Set[str]
    edges: Dict[str, Set[str]]


class PossibleDependenciesAnalyzer:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.runtime_pkgs, self.runtime_virtuals = self.context.runtime_pkgs()

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
            if pkg_name in self.context.libc_pkgs():
                continue

            pkg_cls = self.context.repo.get_pkg_class(pkg_name=pkg_name)
            for name, conditions in pkg_cls.dependencies_by_name(when=True).items():
                if all(
                    self.context.unreachable(pkg_name=pkg_name, when_spec=x) for x in conditions
                ):
                    tty.debug(
                        f"[{__name__}] Not adding {name} as a dep of {pkg_name}, because "
                        f"conditions cannot be met"
                    )
                    continue

                if not self._has_deptypes(
                    conditions, allowed_deps=allowed_deps, strict=strict_depflag
                ):
                    continue

                if self.context.is_virtual(name) and name in virtuals:
                    continue

                dep_names = set()
                if self.context.is_virtual(name):
                    virtuals.add(name)
                    if expand_virtuals:
                        providers = self.context.providers_for(name)
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
                stack.extend([p.name for p in self.context.providers_for(current_spec.name)])
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
            return self.context.is_allowed_on_this_platform(
                pkg_name=pkg_name
            ) and self.context.can_be_installed(pkg_name=pkg_name)
        except spack.repo.UnknownPackageError:
            return False
