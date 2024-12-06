# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------

from spack.package import *


class Gptl(AutotoolsPackage):
    """
    GPTL is a library to instrument C, C++, and Fortran codes for
    performance analysis and profiling.
    """

    homepage = "https://jmrosinski.github.io/GPTL/"
    url = "https://github.com/jmrosinski/GPTL/releases/download/v8.0.3/gptl-8.0.3.tar.gz"

    maintainers("edwardhartnett", "AlexanderRichert-NOAA", "Hang-Lei-NOAA", "jmrosinski")

    version("8.1.1", sha256="b8ee26f7aeedd2a31d565789634e7c380023fe6b65bbf59030884f4dcbce94a5")
    version("8.0.3", sha256="334979c6fe78d4ed1b491ec57fb61df7a910c58fd39a3658d03ad89f077a4db6")
    version("8.0.2", sha256="011f153084ebfb52b6bf8f190835d4bae6f6b5c0ad320331356aa47a547bf2b4")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("pmpi", default=False, description="Build with PMPI support to auto-profile MPI calls")
    variant("papi", default=False, description="Enable built-in support for papi library")
    variant("nestedomp", default=False, description="Build with nested OMP capability")
    variant("disable-unwind", default=False, description="Skip check for libunwind")

    depends_on("mpi")

    def configure_args(self):
        args = []

        if self.spec.satisfies("+pmpi"):
            args.append("--enable-pmpi")
            args.append("CC=" + self.spec["mpi"].mpicc)
            args.append("CXX=" + self.spec["mpi"].mpicxx)
            args.append("FC=" + self.spec["mpi"].mpifc)
            args.append("F90=" + self.spec["mpi"].mpifc)
            args.append("F77=" + self.spec["mpi"].mpif77)

        if self.spec.satisfies("+papi"):
            args.append("--enable-papi")

        if self.spec.satisfies("+nestedomp"):
            args.append("--enable-nestedomp")

        if self.spec.satisfies("+disable-unwind"):
            args.append("--disable-libunwind")

        return args
