# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pnmpi(CMakePackage):
    """PnMPI is a dynamic MPI tool infrastructure that builds on top of
    the standardized PMPI interface."""

    homepage = "https://github.com/LLNL/PnMPI"
    url = "https://github.com/LLNL/PnMPI/releases/download/v1.7/PnMPI-v1.7-full.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.7", sha256="523228bdc220ae417d6812c0766bba698a240d71c69981cb0cb2b09a75ef4a9e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("fortran", default=False, description="Configure PnMPI with Fortran support")
    variant(
        "tests", default=False, description='Build test cases and enable "test" makefile target'
    )

    depends_on("cmake", type="build")
    depends_on("argp-standalone", when="platform=darwin")
    depends_on("binutils")
    depends_on("help2man")
    depends_on("doxygen")
    depends_on("mpi")

    @run_before("cmake")
    def check_fortran(self):
        is_no_fortran_compiler = not self.compiler.f77 and not self.compiler.fc
        if self.spec.satisfies("+fortran"):
            if is_no_fortran_compiler:
                raise InstallError(
                    "pnmpi+fortran requires Fortran compiler " "but no Fortran compiler found!"
                )

    def cmake_args(self):
        args = []
        spec = self.spec
        on_off = {True: "ON", False: "OFF"}

        has_fortran = spec.satisfies("+fortran")
        has_tests = spec.satisfies("+tests")

        args.append("-DENABLE_FORTRAN:BOOL={0}".format(on_off[has_fortran]))
        args.append("-DENABLE_TESTING:BOOL={0}".format(on_off[has_tests]))
        return args
