# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cardioid(CMakePackage):
    """Cardiac simulation suite."""

    homepage = "https://baasic.llnl.gov/comp-bio/cardioid-code"
    git = "https://github.com/LLNL/cardioid.git"
    maintainers("rblake-llnl")

    license("MIT")

    version("develop", branch="master")
    version("elecfem", branch="elec-fem")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("cuda", default=False, description="Build with cuda support")
    variant("mfem", default=False, description="Build with mfem support")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi")
    depends_on("cuda", when="+cuda")
    depends_on("mfem+mpi+superlu-dist+lapack", when="+mfem")
    depends_on("hypre+cuda", when="+mfem+cuda")
    depends_on("cmake@3.1:", type="build")
    depends_on("perl", type="build")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DLAPACK_LIB:PATH=" + ";".join(spec["lapack"].libs.libraries),
            "-DBLAS_LIB:PATH=" + ";".join(spec["blas"].libs.libraries),
            "-DENABLE_OPENMP:BOOL=ON",
            "-DENABLE_MPI:BOOL=ON",
            "-DENABLE_FIND_MPI:BOOL=OFF",
            "-DMPI_C_COMPILER:STRING=" + spec["mpi"].mpicc,
            "-DMPI_CXX_COMPILER:STRING=" + spec["mpi"].mpicxx,
            "-DCMAKE_C_COMPILER:STRING=" + spec["mpi"].mpicc,
            "-DCMAKE_CXX_COMPILER:STRING=" + spec["mpi"].mpicxx,
        ]

        if self.spec.satisfies("+cuda"):
            args.append("-DENABLE_CUDA:BOOL=ON")
            args.append("-DCUDA_TOOLKIT_ROOT:PATH=" + spec["cuda"].prefix)
        else:
            args.append("-DENABLE_CUDA:BOOL=OFF")

        if self.spec.satisfies("+mfem"):
            args.append("-DMFEM_DIR:PATH=" + spec["mfem"].prefix)
        return args
