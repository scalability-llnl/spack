# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Mpigraph(Package):
    """LLNL mpigraph"""

    homepage = "https://github.com/LLNL/mpiGraph"
    git = "https://github.com/LLNL/mpiGraph.git"

    version("main", branch="main")

    depends_on("mpi")
    maintainers("adammoody", "onewayforever", "rminnich")
    license("BSD-3-Clause", checked_by="rminnich")

    version("0.0.1")

    depends_on("mpi")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make()
        install("mpiGraph", os.path.join(prefix.bin, "mpiGraph"))
