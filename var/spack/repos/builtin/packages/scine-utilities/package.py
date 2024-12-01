# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ScineUtilities(CMakePackage):
    """Contains functionality which is used in most SCINE modules."""

    homepage = "https://scine.ethz.ch"
    url = "https://github.com/qcscine/utilities/archive/refs/tags/6.0.0.tar.gz"
    git = "https://github.com/qcscine/utilities.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("6.0.0", sha256="e4387d5562b7442a8e31e4dfc028bacfeb6d12e39f2d8aa6effc6db380863b4a")
    version("5.0.0", sha256="a304c89d9a196fe304f38610dea6b066d74590c0d434e4bd09a9796340700465")

    depends_on("cxx", type="build")  # generated

    resource(
        name="dev",
        url="https://github.com/qcscine/development-utils/archive/refs/tags/5.0.1.tar.gz",
        sha256="089ca500fc191e04a968ea166d2fe80178b227bc2e6d3926523fa2eee5f6492d",
        placement="_dev",
    )

    variant("python", default=False, description="Build Python extension module")

    depends_on("boost+system+filesystem+program_options cxxstd=17 @1.65.0:")
    depends_on("eigen@3:")
    depends_on("googletest", type="build")
    depends_on("lbfgspp", type="build")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-pybind11@2.6.2:", when="+python", type="build")
    depends_on("py-scipy", when="+python", type=("build", "run"))
    depends_on("scine-core")
    depends_on("yaml-cpp")

    extends("python", when="+python")

    def patch(self):
        os.rmdir("dev")
        os.rename("_dev", "dev")

        filter_file(
            "find_package(pybind11 2.6.2 EXACT QUIET)",
            "find_package(pybind11)",
            "dev/cmake/ImportPybind11.cmake",
        )

        filter_file(
            "#include <regex>",
            "#include <regex>\n#include <fstream>",
            "src/Utils/Utils/ExternalQC/Turbomole/TurbomoleHelper.cpp",
        )

        filter_file(
            "#include <iostream>",
            "#include <iostream>\n#include <fstream>",
            "src/Utils/Utils/IO/TurbomoleMinimalBasisfile.cpp",
        )

    def cmake_args(self):
        return [
            self.define("SCINE_BUILD_TESTS", self.run_tests),
            self.define_from_variant("SCINE_BUILD_PYTHON_BINDINGS", "python"),
            self.define("SCINE_MARCH", ""),
            self.define("BOOST_ROOT", self.spec["boost"].prefix),
            self.define("BOOST_LIBRARY_DIR", self.spec["boost"].libs.directories[0]),
            self.define("BOOST_INCLUDE_DIR", self.spec["boost"].headers.directories[0]),
            self.define("BOOST_NO_SYSTEM_PATHS", True),
            self.define("Boost_NO_BOOST_CMAKE", True),
        ]
