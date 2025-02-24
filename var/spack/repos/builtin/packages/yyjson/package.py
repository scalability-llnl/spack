# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Yyjson(CMakePackage):
    """The fastest JSON library in C"""

    homepage = "https://ibireme.github.io/yyjson/doc/doxygen/html/"
    url = "https://github.com/ibireme/yyjson/archive/refs/tags/0.10.0.tar.gz"

    license("MIT", checked_by="pranav-sivaraman")

    version("0.10.0", sha256="0d901cb2c45c5586e3f3a4245e58c2252d6b24bf4b402723f6179523d389b165")

    depends_on("c", type="build")
    depends_on("cxx", type="build")  # TODO: test only dependency, but does not work

    def cmake_args(self):
        return [self.define("YYJSON_BUILD_TESTS", self.run_tests)]
