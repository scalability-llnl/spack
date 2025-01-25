# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Static analysis to optimize input creation for clingo"""
from typing import Set, Tuple

import spack.deptypes as dt
import spack.package_base
import spack.spec


class PossibleDependenciesAnalyzer:
    def possible_dependencies(
        self, *specs: spack.spec.Spec, allowed_deps: dt.DepFlag
    ) -> Tuple[Set[str], Set[str]]:
        virtuals: Set[str] = set()
        real_packages = set(
            spack.package_base.possible_dependencies(
                *specs, virtuals=virtuals, depflag=allowed_deps
            )
        )
        return real_packages, virtuals
