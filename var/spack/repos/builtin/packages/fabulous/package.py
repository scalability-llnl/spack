# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Fabulous(CMakePackage):
    """FABuLOuS (Fast Accurate Block Linear krylOv Solver)
    Library implementing Block-GMres with Inexact Breakdown and Deflated Restarting"""

    homepage = "https://gitlab.inria.fr/solverstack/fabulous/"
    git = "https://gitlab.inria.fr/solverstack/fabulous.git"
    url = "https://gitlab.inria.fr/api/v4/projects/2083/packages/generic/source/v1.1.3/fabulous-1.1.3.tar.gz"
    maintainers("fpruvost")

    version("master", branch="master", submodules=True)
    version("1.1.3", sha256="a75a5461984360286c26b104c1d01ac6cf7c3151bfaa42d8e980eb072981f3ef")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("blasmt", default=False, description="use multi-threaded blas and lapack kernels")
    variant("examples", default=False, description="build examples and tests")

    depends_on("blas")
    depends_on("lapack")

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("FABULOUS_BUILD_C_API", True),
            self.define("FABULOUS_BUILD_Fortran_API", True),
            self.define("FABULOUS_LAPACKE_NANCHECK", True),
            self.define("FABULOUS_USE_CHAMELEON", False),
            self.define_from_variant("FABULOUS_BLASMT", "blasmt"),
            self.define_from_variant("FABULOUS_BUILD_EXAMPLES", "examples"),
            self.define_from_variant("FABULOUS_BUILD_TESTS", "examples"),
        ]

        return args
