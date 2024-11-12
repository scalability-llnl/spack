# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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

    maintainers("hjjvandam")

    homepage = (
        "https://www.icams.de/institute/departments-groups/atomistic-modelling-and-simulation/"
    )
    git = "https://github.com/ICAMS/lammps-user-pace.git"
    url = "https://github.com/ICAMS/lammps-user-pace/archive/e2d941286da81a286adf60cc9ddd2c794dc4a6f2.tar.gz"

    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("GPL-2.0-or-later", checked_by="hjjvandam")
    version(
        "2024.11.9",
        sha256="fac15d79d981353627305f7759c92b64022740f0a8b8c47dc7125967f4650c70",
        url="https://github.com/ICAMS/lammps-user-pace/archive/e2d941286da81a286adf60cc9ddd2c794dc4a6f2.tar.gz"
    )
