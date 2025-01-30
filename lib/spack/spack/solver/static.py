# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Static analysis to optimize input creation for clingo"""
from typing import Dict, Optional, Set, Tuple

import spack.config
import spack.deptypes as dt
import spack.repo
import spack.spec

from .context import Context


class PossibleDependenciesAnalyzer:
    @staticmethod
    def from_config(configuration: spack.config.Configuration) -> "PossibleDependenciesAnalyzer":
        return PossibleDependenciesAnalyzer(Context(configuration=configuration))

    def __init__(self, context: Context):
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
