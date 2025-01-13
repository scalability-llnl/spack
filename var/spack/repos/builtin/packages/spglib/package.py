# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spglib(CMakePackage):
    """C library for finding and handling crystal symmetries."""

    homepage = "https://spglib.readthedocs.io/"
    url = "https://github.com/spglib/spglib/archive/v2.0.2.tar.gz"

    maintainers("RMeli")

    patch("fix_cmake_install.patch", when="@:1.10.3")
    # patch by Krishnendu Ghosh
    patch("fix_cpp.patch", when="@:1.10.3")

    license("BSD-3-Clause")

    version("2.5.0", sha256="b6026f5e85106c0c9ee57e54b9399890d0f29982e20e96ede0428b3efbe6b914")
    version("2.4.0", sha256="e33694b189c6864f719a59c31e2af55301a524fb68ba9fb65f08e95af471847d")
    version("2.3.1", sha256="c295dbea7d2fc9e50639aa14331fef277878c35f00ef0766e688bfbb7b17d44c")
    version("2.3.0", sha256="c05eb869018efe2efe5dcb2654cda19c5dd4c07434874205fa542f7766f7548e")
    version("2.2.0", sha256="ac929e20ec9d4621411e2cdec59b1442e02506c1e546005bbe2c7f781e9bd49a")
    version("2.1.0", sha256="31bca273a1bc54e1cff4058eebe7c0a35d5f9b489579e84667d8e005c73dcc13")
    version("2.0.2", sha256="10e44a35099a0a5d0fc6ee0cdb39d472c23cb98b1f5167c0e2b08f6069f3db1e")
    version("2.0.1", sha256="d7407c0d67174a0c5e41a82ed62948c43fcaf1b5529f97238d7fadd1123ffe22")
    version("2.0.0", sha256="426c4004e84fdb732d86aa5fcada5257ca8bc7a6915c06ced27565176c16ee96")
    version("1.16.5", sha256="1bbde03b6b78da756c07f458bd90d84f3c253841b9b0632db5b72c5961e87aef")
    version("1.16.4", sha256="7a1cdfdb104040e696e887999fd53d83931ba1285aa8fc3c703dcafc38fb1009")
    version("1.16.3", sha256="1dfe313b460f71de90ee8a01d9f2cd250cd59e16836e1bf64924500dd2aa7dc6")
    version("1.16.2", sha256="5723789bee7371ebba91d78c729d2a608f198fad5e1c95eebe18fda9f2914ec8")
    version("1.16.1", sha256="e90682239e4ef63b492fa4e44f7dbcde2e2fe2e688579d96b01f2730dfdf5b2e")
    version("1.16.0", sha256="969311a2942fef77ee79ac9faab089b68e256f21713194969197e7f2bdb14772")
    version("1.15.1", sha256="b6dc2c8adcc7d0edee7a076e765c28b2941b2aeba590d213a0b4893c8af0c026")
    version("1.15.0", sha256="2e217beff6840a22ab2149598eb2f40616b2eeb9e155edab52761d3301412f98")
    version("1.14.1", sha256="9803b0648d9c2d99377f3e1c4cecf712320488403cd674192ec5cbe956bb3c78")
    version("1.14.0", sha256="0a5e518c3dc221386d2219cbd260d08b032b0d2a31bccc32e1a8cb7874e7e9e9")
    version("1.13.0", sha256="ed72ae7bdd129487c45ff7bebb8e2ac03074657060e068b015e7741c0271e16b")
    version("1.12.2", sha256="d92f5e4fa0f54cc0abd0209b81c4d5c647dae9d25b774c2296f44b8558b17976")
    version("1.12.1", sha256="1765e68982425de6d30029d50d200f20425b8ed1deff52b8e73a4a1457ac9ab6")
    version("1.12.0", sha256="79361ef230b4fd55d5eb7521c23430acc3f11ab527125dc324ffb315783ebdfa")
    version("1.11.2.1", sha256="f6795523a04871e012e7f5f5ab97b249fa36657b73cdc9b4ea53ef023cfcaac4")
    version("1.11.2", sha256="aae61218dd0cca1fda245d4ad906c2eed5e8d30e28b575d74eab9a6be26bbd5d")
    version("1.11.1.2", sha256="d99dab24accd269df65c01febd05cb5dd1094a89d7279f8390871f0432df2b56")
    version("1.11.1", sha256="3b5a859f3fe2c9b096fc0754ffbd9341c568bc8003d2eeb74c958c1cacb480f5")
    version("1.11.0", sha256="e4befe27473a69b7982597760d6838cc48d9ef7b624a439436a17f5487f78f51")
    version("1.10.4", sha256="6a15a324a821ad9d3e615e120d9c5e704e284d8eb1f076aa21741a23fbcf08df")
    version("1.10.3", sha256="43776b5fb220b746d53c1aa39d0230f304687ec05984671392bccaf850d9d696")
    version("1.10.2", sha256="5907d0d29563689146512ef24aa8960d9475c5de326501f277bb58b3de21b07d")
    version("1.10.1", sha256="8ed979cda82f6d440567197ec191bffcb82ee83c5bfe8a484c5a008dd00273f0")
    version("1.10.0", sha256="117fff308731784bea2ddaf3d076f0ecbf3981b31ea1c1bfd5ce4f057a5325b1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=True, description="Build with OpenMP support", when="@1.16.2:")
    variant("fortran", default=True, description="Build Fortran interface", when="@1.16.4:")
    variant("tests", default=False, description="Build with tests", when="@2.1.0:")

    depends_on("cmake@3.15:", type="build", when="@2.1.0:")
    depends_on("cmake@3.24:", type="build", when="+tests")

    @property
    def libs(self):
        return find_libraries("libsymspg", root=self.prefix, shared=True, recursive=True)

    def cmake_args(self):
        pfx = "SPGLIB_" if self.spec.satisfies("@2.1.0:") else ""
        return [
            self.define_from_variant(pfx + "USE_OMP", "openmp"),
            self.define_from_variant(pfx + "WITH_Fortran", "fortran"),
            self.define_from_variant(pfx + "WITH_TESTS", "tests"),
        ]
