# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Filo(CMakePackage):
    """File flush and fetch, with MPI"""

    homepage = "https://github.com/ecp-veloc/filo"
    git = "https://github.com/ecp-veloc/filo.git"

    tags = ["ecp"]

    license("MIT")

    version("main", branch="main")

    depends_on("c", type="build")  # generated

    depends_on("mpi")
    depends_on("axl")
    depends_on("kvtree")
    depends_on("spath")

    def cmake_args(self):
        args = []
        args.append("-DMPI_C_COMPILER=%s" % self.spec["mpi"].mpicc)
        args.append("-DWITH_AXL_PREFIX=%s" % self.spec["axl"].prefix)
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec["kvtree"].prefix)
        args.append("-DWITH_SPATH_PREFIX=%s" % self.spec["spath"].prefix)
        return args
