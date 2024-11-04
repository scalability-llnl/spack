# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stdexec(CMakePackage):
    """The proposed C++ framework for asynchronous and parallel programming."""

    homepage = "https://github.com/NVIDIA/stdexec"
    url = "https://github.com/NVIDIA/stdexec/archive/nvhpc-0.0.tar.gz"
    git = "https://github.com/NVIDIA/stdexec.git"
    maintainers("msimberg", "aurianer")

    license("Apache-2.0")

    version("24.09", sha256="d2d811c852dc6c53527a244a54ae343d6b65a50c23ea49f93723e3082435fff4")
    version("23.03", sha256="2c9dfb6e56a190543049d2300ccccd1b626f4bb82af5b607869c626886fadd15")
    version("main", branch="main")

    depends_on("cxx", type="build")

    depends_on("cmake@3.23.1:", type="build")

    conflicts("%gcc@:10")
    conflicts("%clang@:12")

    @when("@:23.03")
    def build(self, spec, prefix):
        pass

    def cmake_args(self):
        return [
            self.define("STDEXEC_BUILD_TESTS", self.run_tests),
            self.define("STDEXEC_BUILD_EXAMPLES", False),
        ]
