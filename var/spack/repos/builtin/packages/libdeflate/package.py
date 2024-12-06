# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import cmake, makefile
from spack.package import *


class Libdeflate(MakefilePackage, CMakePackage):
    """Heavily optimized library for DEFLATE/zlib/gzip compression and decompression"""

    homepage = "https://github.com/ebiggers/libdeflate"
    url = "https://github.com/ebiggers/libdeflate/archive/v1.7.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version("1.18", sha256="225d982bcaf553221c76726358d2ea139bb34913180b20823c782cede060affd")
    version("1.14", sha256="89e7df898c37c3427b0f39aadcf733731321a278771d20fc553f92da8d4808ac")
    version("1.10", sha256="5c1f75c285cd87202226f4de49985dcb75732f527eefba2b3ddd70a8865f2533")
    version("1.7", sha256="a5e6a0a9ab69f40f0f59332106532ca76918977a974e7004977a9498e3f11350")

    depends_on("c", type="build")  # generated

    build_system(
        conditional("makefile", when="@:1.14"),
        conditional("cmake", when="@1.15:"),
        default="cmake",
    )

    depends_on("zlib-api")
    depends_on("gzip")

    with when("build_system=cmake"):
        depends_on("cmake@3.7:", type="build")


class MakefileBuilder(makefile.MakefileBuilder):
    def install(self, pkg, spec, prefix):
        with working_dir(self.build_directory):
            make("install", f"PREFIX={prefix}")


class CMakeBuilder(cmake.CMakeBuilder):
    pass
