# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Ftq(Package):
    """Fixed Time Quantum benchmark"""

    homepage = "https://github.com/rminnich/ftq"
    git = "https://github.com/rminnich/ftq.git"


    maintainers("brho", "rminnich")
    license("GPL", checked_by="rminnich")

    version("master", branch="master")
    version("0.0.1")

    depends_on("mpi")
    depends_on("libpthread-stubs")
    depends_on("r-getoptlong")
    depends_on("gcc", type="build")


    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make("mpiftq")
        install("mpiftq", os.path.join(prefix.bin, "mpiftq"))
        make("mpibarrier")
        install("mpibarrier", os.path.join(prefix.bin, "mpibarrier"))
        make("linux")
        install("ftq.linux", os.path.join(prefix.bin, "ftq.linux"))
