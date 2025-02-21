# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rankstr(CMakePackage):
    """Assign one-to-one mapping of MPI ranks to strings"""

    homepage = "https://github.com/ecp-veloc/rankstr"
    url = "https://github.com/ecp-veloc/rankstr/archive/v0.0.3.tar.gz"
    git = "https://github.com/ecp-veloc/rankstr.git"
    tags = ["ecp"]

    maintainers("CamStan", "gonsie")

    license("MIT")

    version("main", branch="main")
    version("0.4.0", sha256="f33c920aa67b867d0fa2001d98f6762e90f59a41b2f66c27a63cff6bd6afeb1b")
    version("0.3.0", sha256="5e6378a8fe155b4c6c5cf45db8aaf0562d88e93471d0e12c1e922252ffcce5e6")
    version("0.2.0", sha256="a3f7fd8015156c1b600946af759a03e099e05c83e7b2da6bac394fe7c0d4efae")
    version("0.1.0", sha256="b68239d67b2359ecc067cc354f86ccfbc8f02071e60d28ae0a2449f2e7f88001")
    version("0.0.3", sha256="d32052fbecd44299e13e69bf2dd7e5737c346404ccd784b8c2100ceed99d8cd3")
    version("0.0.2", sha256="b88357bf88cdda9565472543225d6b0fa50f0726f6e2d464c92d31a98b493abb")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("mpi")

    variant("shared", default=True, description="Build with shared libraries")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))

        if spec.satisfies("@0.1.0:"):
            args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        return args
