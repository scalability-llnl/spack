# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT

from spack.package import *

class Neofoam(CMakePackage):
    """NeoFOAM is a WIP prototype of a modern CFD core."""

    homepage = "https://github.com/exasim-project/NeoFOAM"
    git = homepage

    # maintainers("greole", "HenningScheufler")

    license("MIT", checked_by="greole")

    version("develop", branch="main")

    depends_on("mpi")
    depends_on("kokkos@4.3.0")
