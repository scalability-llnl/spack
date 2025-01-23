# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FusionIo(CMakePackage):
    """Fusion-IO is a library providing common interface (C++, C, Fortran, Python)
    to data from various fusion simulation codes. It supported reading data from
    M3D-C1, GPEC, MARS, GATO outputs and GEQDSK files."""

    git = "https://github.com/nferraro/fusion-io"

    maintainers("changliu777")

    license("MIT")

    version("master", submodules=True, branch="master")

    variant("python", default=True, description="Enable Python support")
    variant("trace", default=True, description="Build trace program")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    depends_on("mpi")
    depends_on("hdf5")
    depends_on("cmake@3:", type="build")

    extends("python", when="+python")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define("CMAKE_C_COMPILER", spec["mpi"].mpicc),
            self.define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx),
            self.define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc),
            self.define_from_variant("FUSIONIO_ENABLE_TRACE", "trace"),
            self.define_from_variant("FUSIONIO_ENABLE_PYTHON", "python"),
        ]

        if self.spec.satisfies("+python"):
            args.append(self.define("PYTHON_MODULE_INSTALL_PATH", python_platlib))

        return args
