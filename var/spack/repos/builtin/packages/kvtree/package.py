# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kvtree(CMakePackage):
    """KVTree provides a fully extensible C datastructure modeled after perl
    hashes."""

    homepage = "https://github.com/ecp-veloc/KVTree"
    url = "https://github.com/ecp-veloc/KVTree/archive/v1.1.1.tar.gz"
    git = "https://github.com/ecp-veloc/kvtree.git"
    tags = ["ecp"]

    maintainers("CamStan", "gonsie")

    license("MIT")

    version("main", branch="main")
    version("1.4.0", sha256="48a36fd578f0d1198a9c1512d6446c830b915ace5bb97539eec615495bee5a51")
    version("1.3.0", sha256="8281e075772d3534183c46133553d5765455d79ed98a895743663db891755ca9")
    version("1.2.0", sha256="ecd4b8bc479c33ab4f23fc764445a3bb353a1d15c208d011f5577a32c182477f")
    version("1.1.1", sha256="4776bd55a559b7f9bb594454ae6b14ebff0087c93c3d59ac7d1ab27df4aa4d74")
    version("1.1.0", sha256="3e6c003e7b8094d7c2d1529a973d68a68f953ffa63dcde5f4c7c7e81ddf06564")
    version("1.0.3", sha256="c742cdb1241ef4cb13767019204d5350a3c4383384bed9fb66680b93ff44b0d4")
    version("1.0.2", sha256="56fb5b747758c24a907a8380e8748d296900d94de9547bc15f6b427ac4ae2ec4")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api", type="link")

    variant("mpi", default=True, description="Build with MPI message packing")
    depends_on("mpi", when="+mpi")

    variant(
        "file_lock",
        default="FLOCK",
        values=("FLOCK", "FNCTL", "NONE"),
        multi=False,
        description="File locking style for KVTree.",
    )

    variant("shared", default=True, description="Build with shared libraries")

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%cce"):
            if name == "ldflags":
                flags.append("-Wl,-z,muldefs")
        return (flags, None, None)

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define_from_variant("MPI"))
        if spec.satisfies("+mpi"):
            args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))

        args.append(self.define_from_variant("KVTREE_FILE_LOCK", "file_lock"))

        if spec.satisfies("@1.2.0:"):
            args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        return args
