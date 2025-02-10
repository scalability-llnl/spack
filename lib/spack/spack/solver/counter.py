# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
from typing import List, Set

import spack.deptypes as dt
import spack.repo
import spack.spec

from .context import PossibleDependencyGraph


class Counter:
    """Computes the possible packages and the maximum number of duplicates
    allowed for each of them.

    Args:
        specs: abstract specs to concretize
        tests: if True, add test dependencies to the list of possible packages
    """

    def __init__(
        self, specs: List["spack.spec.Spec"], tests: bool, possible_graph: PossibleDependencyGraph
    ) -> None:
        self.possible_graph = possible_graph
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
        self._possible_dependencies, virtuals, _ = self.possible_graph.possible_dependencies(
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
    def __init__(
        self, specs: List["spack.spec.Spec"], tests: bool, possible_graph: PossibleDependencyGraph
    ) -> None:
        super().__init__(specs, tests, possible_graph)
        self._link_run: Set[str] = set()
        self._direct_build: Set[str] = set()
        self._total_build: Set[str] = set()
        self._link_run_virtuals: Set[str] = set()

    def _compute_cache_values(self) -> None:
        self._link_run, virtuals, _ = self.possible_graph.possible_dependencies(
            *self.specs, allowed_deps=self.link_run_types
        )
        self._possible_virtuals.update(virtuals)
        self._link_run_virtuals.update(virtuals)
        for x in self._link_run:
            reals, virtuals, _ = self.possible_graph.possible_dependencies(
                x, allowed_deps=dt.BUILD, transitive=False, strict_depflag=True
            )
            self._possible_virtuals.update(virtuals)
            self._direct_build.update(reals)

        self._total_build, virtuals, _ = self.possible_graph.possible_dependencies(
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
