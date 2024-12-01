# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpilander(CMakePackage):
    """There can only be one (MPI process)!"""

    homepage = "https://github.com/MPILander/MPILander"
    git = "https://github.com/MPILander/MPILander.git"

    maintainers("ax3l")

    license("MIT")

    version("develop", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # variant('cuda', default=False, description='Enable CUDA support')
    # variant(
    #     'schedulers',
    #     description='List of supported schedulers',
    #     values=('alps', 'lsf', 'tm', 'slurm', 'sge', 'loadleveler'),
    #     multi=True
    # )

    depends_on("cmake@3.9.2:", type="build")

    provides("mpi@:3.1")

    # compiler support
    conflicts("%gcc@:4.7")
    conflicts("%clang@:3.8")
    conflicts("%apple-clang@:7.4")
    conflicts("%intel@:16")

    def cmake_args(self):
        args = [
            # tests and examples
            self.define("BUILD_TESTING", self.run_tests),
            self.define("BUILD_EXAMPLES", self.run_tests),
        ]

        return args
