# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MatrixSwitch(CMakePackage):
    """Intermediary interface between high-level routines for
    physics-related algorithms and low-level routines dealing
    with matrix storage and manipulation."""

    homepage = "https://gitlab.com/ElectronicStructureLibrary/omm/matrixswitch"
    url = "https://gitlab.com/ElectronicStructureLibrary/omm/matrixswitch/-/archive/1.2.1/matrixswitch-1.2.1.tar.gz"
    git = "https://gitlab.com/ElectronicStructureLibrary/omm/matrixswitch.git"

    maintainers("RMeli")

    license("BSD-2-Clause", checked_by="RMeli")

    version("1.2.1", sha256="a3c2bac20435a8217cd1a1abefa8b7f8c52b1c6f55a75b2861565ade5ecfe37f")
    version("master", branch="master")

    depends_on("fortran", type="build")  # generated

    variant("lapack", default=True, description="Build with LAPACK interface.")
    variant("mpi", default=True, description="Build with MPI support.")
    variant("scalapack", default=True, when="+mpi", description="Build with ScaLAPACK interface.")
    variant("dbcsr", default=False, when="+mpi", description="Build with DBCSR interface.")

    depends_on("cmake@3.22:", type="build")
    generator("ninja")

    depends_on("lapack", when="+lapack")
    depends_on("mpi", when="+mpi")
    depends_on("scalapack", when="+scalapack")
    depends_on("dbcsr~shared", when="+dbcsr")  # Expects static library (FindCustomDbcsr)

    def cmake_args(self):
        args = [
            self.define_from_variant("WITH_LAPACK", "lapack"),
            self.define_from_variant("WITH_MPI", "mpi"),
            self.define_from_variant("WITH_SCALAPACK", "scalapack"),
            self.define_from_variant("WITH_DBCSR", "dbcsr"),
        ]

        if self.spec.satisfies("+dbcsr"):
            args.append(self.define("DBCSR_ROOT", self.spec["dbcsr"].prefix))

        return args

    @property
    def libs(self):
        return find_libraries("libmatrixswitch", root=self.home, recursive=True, shared=False)
