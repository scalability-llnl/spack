# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack.package import *


class Globalarrays(AutotoolsPackage):
    """Global Arrays (GA) is a Partitioned Global Address Space (PGAS)
    programming model.

    It provides primitives for one-sided communication (Get, Put, Accumulate)
    and Atomic Operations (read increment). It supports blocking and
    non-blocking primtives, and supports location consistency.
    """

    homepage = "https://hpc.pnl.gov/globalarrays/"
    url = "https://github.com/GlobalArrays/ga/releases/download/v5.7/ga-5.7.tar.gz"

    tags = ["e4s"]

    license("BSD-3-Clause")

    version("5.8.2", sha256="51599e4abfe36f05cecfaffa33be19efbe9e9fa42d035fd3f866469b663c22a2")
    version("5.8", sha256="64df7d1ea4053d24d84ca361e67a6f51c7b17ed7d626cb18a9fbc759f4a078ac")
    version("5.7.2", sha256="8cd0fcfd85bc7f9c168c831616f66f1e8b9b2ca31dc7dd93cc55b27cc7fe7069")
    version("5.7.1", sha256="aa4c6038d792cabf1766e264320da58a555da81a3a36be32b7c4d3e71c08ffa9")
    version("5.7", sha256="3ed1ab47adfda7bceb7beca12fc05a2e1631732f0e55bbaf9036dad4e3da4774")
    version("5.6.5", sha256="17a7111dfe67d44cf0888c7b79abd48bf4968874f26b3f16cce9fd04e2c72bb9")
    version("5.6.4", sha256="3daf742053502755c0b581041a56f8f7086af05980c7146d194b0fd6526ee14f")
    version("5.6.3", sha256="e8818825d4f72c8433f416a9ae2bba203a521e9bc73d80f96c2250deaef4bc40")
    version("5.6.2", sha256="3eb1c92d41235f3386e0215f04aaab1aae30a2bce191f9fb6436b2cd8b9544ba")
    version("5.6.1", sha256="b324deed49f930f55203e1d18294ce07dd02680b9ac0728ebc54f94a12557ebc")
    version("5.6", sha256="a228dfbae9a6cfaae34694d7e56f589ac758e959b58f4bc49e6ef44058096767")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("scalapack", default=False, description="Enable SCALAPACK")
    variant(
        "armci",
        values=("mpi-ts", "mpi-pr", "mpi3", "openib", "ofi"),
        default="mpi-ts",
        description="ARMCI runtime",
    )

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")

    depends_on("libfabric", when="armci=ofi")
    depends_on("rdma-core", when="armci=openib")

    depends_on("scalapack", when="+scalapack")

    # See release https://github.com/GlobalArrays/ga/releases/tag/v5.7.1
    conflicts("%gcc@10:", when="@5.7")
    conflicts("%gcc@10:", when="@:5.6.5")

    @property
    def build_directory(self):
        return os.path.join(str(self.stage.source_path), "..", "spack-build")

    def configure_args(self):
        blas_flags = self.spec["blas"].libs.ld_flags
        lapack_libs = self.spec["lapack"].libs.ld_flags

        args = [
            "--enable-shared",
            "--with-mpi",
            "--with-blas={0}".format(blas_flags),
            "--with-lapack={0}".format(lapack_libs),
        ]

        if self.spec.satisfies("+scalapack"):
            scalapack_libs = self.spec["scalapack"].libs.ld_flags
            args.append("--with-scalapack={0}".format(scalapack_libs))

        args.append("--with-" + self.spec.variants["armci"].value)

        return args
