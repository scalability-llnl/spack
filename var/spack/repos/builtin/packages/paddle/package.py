# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Paddle(CMakePackage):
    """Parallel algebraic domain decomposition for linear algebra software package."""

    homepage = "https://gitlab.inria.fr/solverstack/paddle"
    git = "https://gitlab.inria.fr/solverstack/paddle.git"
    maintainers("fpruvost")

    version("master", branch="master", submodules=True)
    version("0.3.7", tag="0.3.7", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("parmetis", default=False, description="Enable ParMETIS ordering")
    variant("tests", default=False, description="Enable tests")

    depends_on("mpi")
    depends_on("scotch~metis+mpi")
    depends_on("parmetis", when="+parmetis")

    root_cmakelists_dir = "src"

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define_from_variant("PADDLE_ORDERING_PARMETIS", "parmetis"),
            self.define_from_variant("PADDLE_BUILD_TESTS", "tests"),
        ]

        return args
