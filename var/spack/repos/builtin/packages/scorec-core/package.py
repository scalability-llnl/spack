# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ScorecCore(CMakePackage):
    """The SCOREC Core is a set of C/C++ libraries for unstructured mesh
    simulations on supercomputers.
    """

    homepage = "https://www.scorec.rpi.edu/"
    git = "https://github.com/SCOREC/core.git"

    license("BSD-3-Clause")

    version("develop")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("zoltan")
    depends_on("cmake@3.0:", type="build")

    def cmake_args(self):
        options = []
        options.append("-DCMAKE_C_COMPILER=%s" % self.spec["mpi"].mpicc)
        options.append("-DCMAKE_CXX_COMPILER=%s" % self.spec["mpi"].mpicxx)
        options.append("-DENABLE_ZOLTAN=ON")

        if self.compiler.name == "xl":
            options.append("-DSCOREC_EXTRA_CXX_FLAGS=%s" % "-qminimaltoc")

        return options
