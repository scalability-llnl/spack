# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Vpic(CMakePackage):
    """VPIC is a general purpose particle-in-cell simulation code for modeling
    kinetic plasmas in one, two, or three spatial dimensions. It employs a
    second-order, explicit, leapfrog algorithm to update charged particle
    positions and velocities in order to solve the relativistic kinetic
    equation for each species in the plasma, along with a full Maxwell
    description for the electric and magnetic fields evolved via a second-
    order finite-difference-time-domain (FDTD) solve.
    """

    homepage = "https://github.com/lanl/vpic"
    git = "https://github.com/lanl/vpic.git"

    license("BSD-3-Clause")

    version("develop", branch="master", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build")
    depends_on("mpi")

    def cmake_args(self):
        options = ["-DENABLE_INTEGRATED_TESTS=ON", "-DENABLE_UNIT_TESTS=ON"]

        return options
