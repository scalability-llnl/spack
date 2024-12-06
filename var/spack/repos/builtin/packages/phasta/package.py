# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Phasta(CMakePackage):
    """SCOREC RPI's Parallel Hierarchic Adaptive Stabilized Transient Analysis
    (PHASTA) of compressible and incompressible Navier Stokes equations."""

    homepage = "https://www.scorec.rpi.edu/software.php"
    git = "https://github.com/PHASTA/phasta.git"

    license("BSD-3-Clause")

    version("develop", branch="master")
    version("0.0.1", commit="11f431f2d1a53a529dab4b0f079ab8aab7ca1109")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DPHASTA_USE_MPI=ON",
            "-DPHASTA_BUILD_CONVERTERIO=OFF",
            "-DPHASTA_BUILD_ACUSTAT=OFF",
            "-DPHASTA_BUILD_M2N=OFF",
            "-DPHASTA_BUILD_M2NFixBnd=OFF",
            "-DPHASTA_USE_LESLIB=OFF",
            "-DPHASTA_USE_PETSC=OFF",
            "-DPHASTA_USE_SVLS=ON",
            "-DPHASTA_INCOMPRESSIBLE=ON",
            "-DPHASTA_COMPRESSIBLE=ON",
            "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
            "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
            "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
        ]

        return args
