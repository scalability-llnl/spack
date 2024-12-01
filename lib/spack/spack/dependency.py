# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Data structures that represent Spack's dependency relationships."""
from typing import Dict, List

import spack.deptypes as dt
import spack.spec


class Dependency:
    """Class representing metadata for a dependency on a package.

    This class differs from ``spack.spec.DependencySpec`` because it
    represents metadata at the ``Package`` level.
    ``spack.spec.DependencySpec`` is a descriptor for an actual package
    configuration, while ``Dependency`` is a descriptor for a package's
    dependency *requirements*.

    A dependency is a requirement for a configuration of another package
    that satisfies a particular spec.  The dependency can have *types*,
    which determine *how* that package configuration is required,
    e.g. whether it is required for building the package, whether it
    needs to be linked to, or whether it is needed at runtime so that
    Spack can call commands from it.

    A package can also depend on another package with *patches*. This is
    for cases where the maintainers of one package also maintain special
    patches for their dependencies.  If one package depends on another
    with patches, a special version of that dependency with patches
    applied will be built for use by the dependent package.  The patches
    are included in the new version's spec hash to differentiate it from
    unpatched versions of the same package, so that unpatched versions of
    the dependency package can coexist with the patched version.

    """

    def __init__(
        self,
        pkg: "spack.package_base.PackageBase",
        spec: "spack.spec.Spec",
        depflag: dt.DepFlag = dt.DEFAULT,
    ):
        """Create a new Dependency.

        Args:
            pkg: Package that has this dependency
            spec: Spec indicating dependency requirements
            type: strings describing dependency relationship
        """
        assert isinstance(spec, spack.spec.Spec)

        self.pkg = pkg
        self.spec = spec.copy()

        # This dict maps condition specs to lists of Patch objects, just
        # as the patches dict on packages does.
        self.patches: Dict[spack.spec.Spec, "List[spack.patch.Patch]"] = {}
        self.depflag = depflag

    @property
    def name(self) -> str:
        """Get the name of the dependency package."""
        return self.spec.name

    def merge(self, other: "Dependency"):
        """Merge constraints, deptypes, and patches of other into self."""
        self.spec.constrain(other.spec)
        self.depflag |= other.depflag

        # concatenate patch lists, or just copy them in
        for cond, p in other.patches.items():
            if cond in self.patches:
                current_list = self.patches[cond]
                current_list.extend(p for p in other.patches[cond] if p not in current_list)
            else:
                self.patches[cond] = other.patches[cond]

    def __repr__(self) -> str:
        types = dt.flag_to_chars(self.depflag)
        if self.patches:
            return f"<Dependency: {self.pkg.name} -> {self.spec} [{types}, {self.patches}]>"
        else:
            return f"<Dependency: {self.pkg.name} -> {self.spec} [{types}]>"
