# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import cmake
from spack.package import *


class JsonC(CMakePackage, AutotoolsPackage):
    """A JSON implementation in C."""

    homepage = "https://github.com/json-c/json-c/wiki"
    url = "https://s3.amazonaws.com/json-c_releases/releases/json-c-0.15.tar.gz"

    license("MIT")

    version("0.18", sha256="876ab046479166b869afc6896d288183bbc0e5843f141200c677b3e8dfb11724")
    version("0.16", sha256="8e45ac8f96ec7791eaf3bb7ee50e9c2100bbbc87b8d0f1d030c5ba8a0288d96b")
    version("0.15", sha256="b8d80a1ddb718b3ba7492916237bbf86609e9709fb007e7f7d4322f02341a4c6")
    version("0.14", sha256="b377de08c9b23ca3b37d9a9828107dff1de5ce208ff4ebb35005a794f30c6870")

    with default_args(deprecated=True):
        version(
            "0.13.1", sha256="b87e608d4d3f7bfdd36ef78d56d53c74e66ab278d318b71e6002a369d36f4873"
        )
        version(
            "0.12.1", sha256="2a136451a7932d80b7d197b10441e26e39428d67b1443ec43bbba824705e1123"
        )
        version("0.12", sha256="000c01b2b3f82dcb4261751eb71f1b084404fb7d6a282f06074d3c17078b9f3f")
        version("0.11", sha256="28dfc65145dc0d4df1dfe7701ac173c4e5f9347176c8983edbfac9149494448c")

    depends_on("c", type="build")

    build_system(
        conditional("cmake", when="@0.14:"),
        conditional("autotools", when="@:0.13"),
        default="cmake",
    )

    depends_on("autoconf", when="build_system=autotools", type="build")
    depends_on("cmake@3.9:", when="@0.17: build_system=cmake", type="build")

    @property
    def parallel(self):
        # autotools issue with make -j: https://github.com/json-c/json-c/issues/75
        return not self.spec.satisfies("build_system=autotools")


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        return [self.define("DISABLE_WERROR", True)]
