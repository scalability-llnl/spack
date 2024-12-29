# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GoblinHmcSim(MakefilePackage):
    """
    The Goblin HMC-Sim is a Hybrid Memory Cube
    Functional Simulation Environment
    """

    homepage = "https://github.com/tactcomplabs/gc64-hmcsim"
    git = "https://github.com/tactcomplabs/gc64-hmcsim"
    # The version numbers track the SST they were released with
    url = "https://github.com/tactcomplabs/gc64-hmcsim/archive/refs/tags/sst-8.0.0-release.tar.gz"
    # This works with parallel builds outside Spack
    # For some reason .o files get thrashed inside Spack
    parallel = False

    maintainers("berquist")

    license("BSD-2-Clause")

    version("8.0.0", sha256="8a5e6b701865a581f15965d3ddd8c7d301b15f4b63543c444058e9c3688fd2c8")

    version("main", branch="main")

    def install(self, spec, prefix):
        install_tree(".", prefix)
