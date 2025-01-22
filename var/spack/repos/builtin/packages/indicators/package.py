# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Indicators(CMakePackage):
    """Activity indicators for modern C++."""

    homepage = "https://github.com/p-ranav/indicators"
    url = "https://github.com/p-ranav/indicators/archive/refs/tags/v2.3.tar.gz"
    list_url = "https://github.com/p-ranav/indicators/tags"
    git = "https://github.com/p-ranav/indicators.git"

    maintainers("stephenswat")

    license("MIT", checked_by="stephenswat")

    version("2.3", sha256="70da7a693ff7a6a283850ab6d62acf628eea17d386488af8918576d0760aef7b")

    depends_on("cxx", type="build")
    depends_on("cmake@3.8:", type="build")

    def cmake_args(self):
        args = [
            self.define("INDICATORS_BUILD_TESTS", self.run_tests),
            self.define("INDICATORS_SAMPLES", False),
            self.define("INDICATORS_DEMO", False),
        ]
        return args
