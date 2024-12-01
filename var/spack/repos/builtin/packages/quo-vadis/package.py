# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class QuoVadis(CMakePackage):
    """A cross-stack coordination layer to dynamically
    map runtime components to hardware resources"""

    homepage = "https://github.com/hpc/quo-vadis"
    git = "https://github.com/hpc/quo-vadis.git"

    maintainers("samuelkgutierrez")

    license("BSD-3-Clause")

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("fortran", default=True, description="Build with Fortran bindings")
    variant("mpi", default=True, description="Build with MPI support")
    variant("mpipat", default=False, description="Affirm MPI processes are threads")
    variant("omp", default=True, description="Build with OpenMP support")

    variant(
        "gpu",
        values=("nvidia", "amd", "none"),
        default="none",
        multi=True,
        description="Build with GPU support",
    )

    depends_on("libzmq")

    with when("+mpi"):
        depends_on("mpi")

    with when("gpu=nvidia"):
        depends_on("libpciaccess")
        depends_on("cuda")

    with when("gpu=amd"):
        depends_on("libpciaccess")
        depends_on("rocm-smi-lib")

    def cmake_args(self):
        spec = self.spec

        return [
            self.define_from_variant("QV_FORTRAN_SUPPORT", "fortran"),
            self.define_from_variant("QV_MPI_SUPPORT", "mpi"),
            self.define_from_variant("QV_MPI_PROCESSES_ARE_THREADS", "mpipat"),
            self.define_from_variant("QV_OMP_SUPPORT", "omp"),
            self.define("QV_GPU_SUPPORT", not spec.satisfies("gpu=none")),
        ]
