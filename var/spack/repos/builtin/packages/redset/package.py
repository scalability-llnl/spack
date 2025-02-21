# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Redset(CMakePackage, CudaPackage):
    """Create MPI communicators for disparate redundancy sets"""

    homepage = "https://github.com/ecp-veloc/redset"
    url = "https://github.com/ecp-veloc/redset/archive/v0.0.5.tar.gz"
    git = "https://github.com/ecp-veloc/redset.git"
    tags = ["ecp"]

    maintainers("CamStan", "gonsie")

    license("MIT")

    version("main", branch="main")
    version("0.4.0", sha256="d278a5d3c1323915c379e2077dbfab1248044c86a04fc56faee6681c66380451")
    version("0.3.0", sha256="007ca5e7e5f4400e22ad7bca82e366cd51c73f28067c955cc16d7d0ff0c06a1b")
    version("0.2.0", sha256="0438b0ba56dafcd5694a8fceeb5a932901307353e056ab29817d30b8387f787f")
    version("0.1.0", sha256="baa75de0d0d6de64ade50cff3d38ee89fd136ce69869182bdaefccf5be5d286d")
    version("0.0.5", sha256="4db4ae59ab9d333a6d1d80678dedf917d23ad461c88b6d39466fc4bf6467d1ee")
    version("0.0.4", sha256="c33fce458d5582f01ad632c6fae8eb0a03eaef00e3c240c713b03bb95e2787ad")
    version("0.0.3", sha256="30ac1a960f842ae23a960a88b312af3fddc4795f2053eeeec3433a61e4666a76")

    depends_on("c", type="build")  # generated

    depends_on("mpi")
    depends_on("kvtree+mpi")
    depends_on("rankstr")
    depends_on("zlib-api", type="link")

    depends_on("kvtree@:1.3.0", when="@:0.2.0")
    depends_on("kvtree@1.4.0:", when="@0.3.0:")
    depends_on("rankstr@:0.2.0", when="@:0.2.0")
    depends_on("rankstr@0.3.0:", when="@0.3.0:")

    variant("cuda", default=False, description="Enable CUDA support", when="@0.4:")
    variant("openmp", default=False, description="Enable OpenMP support", when="@0.4:")
    variant("pthreads", default=False, description="Enable Pthread support", when="@0.4:")

    variant("shared", default=True, description="Build with shared libraries", when="@0.1:")
    depends_on("kvtree+shared", when="@0.1: +shared")
    depends_on("kvtree~shared", when="@0.1: ~shared")
    depends_on("rankstr+shared", when="@0.1: +shared")
    depends_on("rankstr~shared", when="@0.1: ~shared")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))
        args.append(self.define("WITH_KVTREE_PREFIX", spec["kvtree"].prefix))
        args.append(self.define("WITH_RANKSTR_PREFIX", spec["rankstr"].prefix))

        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("ENABLE_CUDA", "cuda"))
        args.append(self.define_from_variant("ENABLE_OPENMP", "openmp"))
        args.append(self.define_from_variant("ENABLE_PTHREADS", "pthreads"))

        return args
