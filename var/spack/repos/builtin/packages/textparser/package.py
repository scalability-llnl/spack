# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Textparser(CMakePackage):
    """Text Parser library allows us to describe and to parse JSON like
    simple parameter structure."""

    homepage = "https://github.com/avr-aics-riken/TextParser"
    git = "https://github.com/avr-aics-riken/TextParser.git"

    license("BSD-2-Clause")

    version("master", branch="master")
    version("1.8.8", commit="31ec1f23df21611d0765c27a6458fdbbf4cde66d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Activate MPI support")
    variant("fapi", default=False, description="This option is for building Fortran API.")
    variant(
        "test",
        default=False,
        description="This option turns on compiling sample codes and" + " execute the tests.",
    )

    patch("fix_compiler_options.patch")

    depends_on("mpi", when="+mpi")

    parallel = False

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append("-DINSTALL_DIR={0}".format(self.prefix))

        if "+mpi" in spec:
            args.append("-Dwith_MPI=yes")
            args.append("-DCMAKE_CXX_COMPILER=" + spec["mpi"].mpicxx)
        else:
            args.append("-Dwith_MPI=no")

        if "+fapi" in spec:
            args.append("-Denable_fapi=yes")
        else:
            args.append("-Denable_fapi=no")

        if "+test" in spec:
            args.append("-Denable_test=yes")
        else:
            args.append("-Denable_test=no")

        if "%fj" in spec:
            args.append("-DCMAKE_TOOLCHAIN_FILE=./cmake/Toolchain_fx100.cmake")

        return args
