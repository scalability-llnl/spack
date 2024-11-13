# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Omm(CMakePackage):
    """Solution of Kohn-Sham equations using the Orbital Minimization Method (OMM)."""

    homepage = "https://gitlab.com/ElectronicStructureLibrary/omm/libomm"
    url = "https://gitlab.com/ElectronicStructureLibrary/omm/libomm/-/archive/1.2.1/libomm-1.2.1.tar.gz"
    git = "https://gitlab.com/ElectronicStructureLibrary/omm/libomm.git"

    maintainers("RMeli")

    license("BSD-2-Clause", checked_by="RMeli")

    version("1.2.1", sha256="4876990056efabdd83b0caad52ed56632d9926b61d73fe3efbd04d0f8d242ede")
    version("master", branch="master")

    depends_on("fortran", type="build")  # generated

    variant("lapack", default=True, description="Build libOMM with LAPACK interface.")
    variant("mpi", default=True, description="Build libOMM with MPI support.")
    variant(
        "scalapack",
        default=True,
        when="+mpi",
        description="Build libOMM with ScaLAPACK interface.",
    )
    variant("dbcsr", default=False, when="+mpi", description="Build libOMM with DBCSR interface.")

    depends_on("cmake@3.22:", type="build")
    generator("ninja")

    depends_on("lapack", when="+lapack")
    depends_on("mpi", when="+mpi")
    depends_on("scalapack", when="+scalapack")
    depends_on("dbcsr~shared", when="+dbcsr")  # Expects static library (FindCustomDbcsr)

    depends_on("matrix-switch")
    depends_on("matrix-switch+lapack", when="+lapack")
    depends_on("matrix-switch+mpi", when="+mpi")
    depends_on("matrix-switch+scalapack", when="+scalapack")
    depends_on("matrix-switch+dbcsr", when="+dbcsr")

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
