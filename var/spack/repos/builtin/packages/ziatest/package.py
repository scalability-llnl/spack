# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Ziatest(MakefilePackage):
    """Realistic assessment of both launch and wireup requirements of MPI applications"""

    homepage = "https://gitlab.com/NERSC/N10-benchmarks/ziatest"
    git = "https://gitlab.com/NERSC/N10-benchmarks/ziatest"
    maintainers("giordano")

    license("custom")

    executables = ["^ziatest$", "^ziaprobe$"]

    version("main", branch="main")

    depends_on("c", type="build")
    depends_on("mpi")

    @property
    def build_targets(self):
        spec = self.spec
        return [f"MPICC={spec['mpi'].mpicc}"]

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("ziatest", prefix.bin)
        install("ziaprobe", prefix.bin)
