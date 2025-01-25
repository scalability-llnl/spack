# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Static analysis to optimize input creation for clingo"""
from typing import Set, Tuple

import spack.deptypes as dt
import spack.repo
import spack.spec


class PossibleDependenciesAnalyzer:
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
                        for p in spack.repo.PATH.providers_for(current_spec.name)
                    ]
                )
                continue
            packages.append((current_spec, current_spec.package_class))

        visited = {}
        for input_spec, pkg in packages:
            pkg.possible_dependencies(
                visited=visited,
                transitive=True,
                expand_virtuals=True,
                depflag=allowed_deps,
                virtuals=virtuals,
            )

        real_packages = set(visited)
        return real_packages, virtuals
