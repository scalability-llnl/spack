# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Neofoam(CMakePackage):
    """NeoFOAM is a WIP prototype of a modern CFD core."""

    homepage = "https://github.com/exasim-project/NeoFOAM"
    git = "https://github.com/exasim-project/NeoFOAM.git"

    maintainers("greole", "HenningScheufler")

    license("MIT", checked_by="greole")

    version("main", branch="main")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("mpi")
    depends_on("kokkos@4.3.0")
