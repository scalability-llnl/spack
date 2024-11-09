# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Composyx(CMakePackage):
    """a Massively Parallel Hybrid Solver in C++"""

    homepage = "https://gitlab.inria.fr/composyx/composyx"
    git = "https://gitlab.inria.fr/composyx/composyx.git"
    url = "https://gitlab.inria.fr/api/v4/projects/52455/packages/generic/source/v1.0.1/composyx-1.0.1.tar.gz"
    maintainers("fpruvost")

    version("main", branch="main", submodules=True)
    version("1.0.1", sha256="d97936e3b297fde435c165cbe29cb39e5d88ae368be451b1c45b8ee51486782c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # User options
    variant("armadillo", default=False, description="Enable Armadillo interface")
    variant("arpack-ng", default=True, description="Enable arpack eigen/singular value solvers")
    variant("eigen", default=True, description="Enable Eigen interface")
    variant("fabulous", default=True, description="Enable Fabulous Iterative Block Krylov solvers")
    variant("paddle", default=True, description="Enable Paddle for matrix partitioning")
    variant("pastix", default=True, description="Enable Pastix sparse direct solver")

    # Executables to compile
    variant("examples", default=True, description="Compile examples")
    variant("tests", default=False, description="Compile tests")

    # Required dependencies
    depends_on("pkgconfig", type="build")
    depends_on("blaspp")
    depends_on("lapackpp")
    depends_on("mpi")

    # Optional dependencies
    depends_on("armadillo", when="+armadillo")
    depends_on("arpack-ng+icb", when="+arpack-ng")
    depends_on("eigen", when="+eigen")
    depends_on("fabulous", when="+fabulous")
    depends_on("paddle", when="+paddle")
    depends_on("pastix+mpi", when="+pastix")

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("COMPOSYX_C_DRIVER", True),
            self.define("COMPOSYX_Fortran_DRIVER", True),
            self.define("COMPOSYX_COMPILE_BENCH", False),
            self.define("COMPOSYX_USE_MUMPS", False),
            self.define("COMPOSYX_USE_QRMUMPS", False),
            self.define("COMPOSYX_USE_SZ_COMPRESSOR", False),
            self.define_from_variant("COMPOSYX_COMPILE_EXAMPLES", "examples"),
            self.define_from_variant("COMPOSYX_COMPILE_TESTS", "tests"),
            self.define_from_variant("COMPOSYX_USE_ARMADILLO", "armadillo"),
            self.define_from_variant("COMPOSYX_USE_ARPACK", "arpack-ng"),
            self.define_from_variant("COMPOSYX_USE_EIGEN", "eigen"),
            self.define_from_variant("COMPOSYX_USE_FABULOUS", "fabulous"),
            self.define_from_variant("COMPOSYX_USE_PADDLE", "paddle"),
            self.define_from_variant("COMPOSYX_USE_PASTIX", "pastix"),
        ]

        return args
