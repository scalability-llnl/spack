# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shuffile(CMakePackage):
    """Shuffle files between MPI ranks"""

    homepage = "https://github.com/ecp-veloc/shuffile"
    url = "https://github.com/ecp-veloc/shuffile/archive/v0.0.4.tar.gz"
    git = "https://github.com/ecp-veloc/shuffile.git"
    tags = ["ecp"]

    maintainers("CamStan", "gonsie")

    license("MIT")

    version("main", branch="main")
    version("0.4.0", sha256="fc7116d8eaa1ab79480e6e3f04064750e517d2a8aeccbff90c73a2590f726378")
    version("0.3.0", sha256="3463ad4a23fd31aa9a3426346ada04399fb9369dd1f40d22df9f19f9c0c1f8ae")
    version("0.2.0", sha256="467ffef72214c109b69f09d03e42be5e9254f13751b09c71168c14fa99117521")
    version("0.1.0", sha256="9e730cc8b7937517a9cffb08c031d9f5772306341c49d17b87b7f349d55a6d5e")
    version("0.0.4", sha256="f0249ab31fc6123103ad67b1eaf799277c72adcf0dfcddf8c3a18bad2d45031d")
    version("0.0.3", sha256="a3f685526a1146a5ad8dbacdc5f9c2e1152d9761a1a179c1db34f55afc8372f6")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("mpi")
    depends_on("kvtree+mpi")
    depends_on("zlib-api", type="link")

    depends_on("kvtree@:1.3.0", when="@:0.2.0")
    depends_on("kvtree@1.4.0:", when="@0.3.0:")

    variant("shared", default=True, description="Build with shared libraries")
    depends_on("kvtree+shared", when="@0.1: +shared")
    depends_on("kvtree~shared", when="@0.1: ~shared")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))
        args.append(self.define("WITH_KVTREE_PREFIX", spec["kvtree"].prefix))

        if spec.satisfies("@0.1.0:"):
            args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        return args
