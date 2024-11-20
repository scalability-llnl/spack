# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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

    depends_on("mpi")
    depends_on("hdf5")
    depends_on("cmake@3:", type="build")

    extends("python", when="+python")

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
            "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
            "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
            self.define_from_variant("FUSIONIO_ENABLE_TRACE", "trace"),
        ]

        if self.spec.variants["python"].value:
            args.extend(["-DFUSIONIO_ENABLE_PYTHON:BOOL=ON"])
            args.append(self.define("PYTHON_MODULE_INSTALL_PATH", python_platlib))

        return args
