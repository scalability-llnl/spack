# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# dlaf-no-license-check
from spack.package import *


class DlaFutureFortran(CMakePackage):
    """
    Fortran interface to the DLA-Future library.
    """

    homepage = "https://github.com/eth-cscs/DLA-Future-Fortran"
    url = "https://github.com/eth-cscs/DLA-Future-Fortran/archive/v0.0.0.tar.gz"
    git = "https://github.com/eth-cscs/DLA-Future-Fortran.git"

    maintainers("RMeli", "rasolca", "aurianer")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("0.2.0", sha256="7fd3e1779c111b35f0d2701a024398b4f6e8dea4af523b6c8617d28c0b7ae61a")
    version("0.1.0", sha256="9fd8a105cbb2f3e1daf8a49910f98fce68ca0b954773dba98a91464cf2e7c1da")

    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries.")
    variant("test", default=False, description="Build tests.")

    generator("ninja")
    depends_on("cmake@3.22:", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("dla-future@0.4.1:0.5 +scalapack", when="@0.1.0")
    depends_on("dla-future@0.6.0: +scalapack", when="@0.2.0:")
    depends_on("dla-future +shared", when="+shared")

    depends_on("mpi", when="+test")
    depends_on("py-fypp", when="+test", type="build")

    def cmake_args(self):
        args = []

        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        if self.spec.satisfies("+test"):
            args.append(self.define("DLAF_FORTRAN_BUILD_TESTING", True))
            # Tests run with 6 MPI ranks
            args.append(self.define("MPIEXEC_MAX_NUMPROCS", 6))

        return args

    @property
    def libs(self):
        return find_libraries(
            "libDLAF_Fortran", root=self.home, shared=self.spec.satisfies("+shared")
        )
