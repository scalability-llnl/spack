# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pmlib(CMakePackage):
    """This library records the statistics information of run-time performance
    and the trace information of a user code and reports its summary.
    The PMlib is able to use for both serial and parallel environments
    including hybrid(OpenMP & MPI) code. In addition, PAPI interface allows
    us to access the information of build-in hardware counter."""

    homepage = "https://github.com/avr-aics-riken/PMlib"
    git = "https://github.com/avr-aics-riken/PMlib.git"

    license("BSD-2-Clause")

    version("master", branch="master")
    version("6.4.1", commit="0a35f5bec8c12e532e5a1bdac8c32c659fd3ee11")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Activate MPI support")
    variant("example", default=False, description="This option turns on compiling sample codes.")
    variant("fortran", default=False, description="This option tells a compiler to use a Fortran.")
    variant("openmp", default=False, description="Enable OpenMP directives")
    variant("papi", default=False, description="Use PAPI library")
    variant("otf", default=False, description="Use OTF library")
    variant(
        "precisetimer",
        default=True,
        description="This option provides -DUSE_PRECISE_TIMER to C++"
        + " compiler option CMAKE_CXX_FLAGS when building"
        + " the PMlib library.",
    )

    patch("fix_compiler_options.patch")

    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append("-DINSTALL_DIR={0}".format(self.prefix))

        if "+mpi" in spec:
            args.append("-Dwith_MPI=yes")
        else:
            args.append("-Dwith_MPI=no")

        if "+example" in spec:
            args.append("-Dwith_example=yes")
        else:
            args.append("-Dwith_example=no")

        if "+fortran" in spec:
            args.append("-Denable_Fortran=yes")
        else:
            args.append("-Denable_Fortran=no")

        if "+openmp" in spec:
            args.append("-Denable_OPENMP=yes")
        else:
            args.append("-Denable_OPENMP=no")

        if "+papi" in spec:
            args.append("-Dwith_PAPI=yes")
        else:
            args.append("-Dwith_PAPI=no")

        if "+otf" in spec:
            args.append("-Dwith_OTF=yes")
        else:
            args.append("-Dwith_OTF=no")

        if "+precisetimer" in spec:
            args.append("-Denable_PreciseTimer=yes")
        else:
            args.append("-Denable_PreciseTimer=no")

        if "%gcc" in spec:
            args.append("-DCMAKE_CXX_FLAGS=-fopenmp")
            args.append("-DCMAKE_Fortran_FLAGS=-fopenmp -cpp")

        if "%fj" in spec:
            args.append("-DCMAKE_TOOLCHAIN_FILE=./cmake/Toolchain_fx100.cmake")

        return args
