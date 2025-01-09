# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class KokkosTools(CMakePackage):
    """Kokkos Profiling and Debugging Tools"""

    homepage = "https://github.com/kokkos/kokkos-tools/"
    git = "https://github.com/kokkos/kokkos-tools.git"

    license("Apache-2.0 WITH LLVM-exception")

    version("develop", branch="develop")

    variant("mpi", default=False, description="Enable MPI support")
    variant("papi", default=False, description="Enable PAPI support")

    depends_on("kokkos")
    depends_on("mpi", when="+mpi")
    depends_on("papi", when="+papi")

    def cmake_args(self):
        args = [
            self.define_from_variant("KokkosTools_ENABLE_MPI", "mpi"),
            self.define_from_variant("KokkosTools_ENABLE_PAPI", "papi"),
        ]
        return args
