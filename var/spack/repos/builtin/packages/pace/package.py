# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pace(CMakePackage):
    """interatomic Potentials in Atomic Cluster Expansion (PACE)

    This library is required to build the ML-PACE module
    in LAMMPS.

    The library was developed at the Interdisciplinary Centre
    for Advanced Materials Simulation (ICAMS), Ruhr University Bochum

    See `Phys Rev Mat 6 013804 (2022)<https://doi.org/10.1103/PhysRevMaterials.6.013804>`__ and
    `Phys Rev B 99 014104 (2019)<https://doi.org/10.1103/PhysRevB.99.014104>`__ for details.
    """

    maintainers("hjjvandam", "rbberger")

    homepage = (
        "https://www.icams.de/institute/departments-groups/atomistic-modelling-and-simulation/"
    )
    git = "https://github.com/ICAMS/lammps-user-pace.git"

    license("GPL-2.0-or-later", checked_by="hjjvandam")
    version("main", branch="main")
    version(
        "2023.11.25.2", tag="v.2023.11.25.fix2", commit="e60e850359b918ca93a5e9329548a58d31f4b12b"
    )

    variant("pic", default=True, description="Build position independent code")

    depends_on("yaml-cpp")
    depends_on("cnpy")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic")]
        return args
