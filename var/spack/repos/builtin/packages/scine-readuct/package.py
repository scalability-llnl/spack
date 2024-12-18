# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ScineReaduct(CMakePackage):
    """
    ReaDuct allows you to carry out structure optimizations, transition state searches
    and intrinsic reaction coordinate (IRC) calculations among other things
    """

    homepage = "https://scine.ethz.ch/download/readuct"
    url = "https://github.com/qcscine/readuct/archive/refs/tags/4.1.0.tar.gz"

    license("BSD-3-Clause")

    version("4.1.0", sha256="9cec0192a444403d6a8fd096509798c49fbd1eec298ec7194aba915e31f50782")

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
    depends_on("googletest")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-pybind11@2.6.2:", when="+python", type=("build", "run"))
    depends_on("scine-core")
    depends_on("scine-utilities")
    depends_on("scine-utilities+python", when="+python", type=("build", "run"))
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

    def cmake_args(self):
        return [
            self.define("SCINE_BUILD_TESTS", self.run_tests),
            self.define("SCINE_BUILD_PYTHON_BINDINGS", "+python" in self.spec),
            self.define("SCINE_MARCH", ""),
            self.define("BOOST_ROOT", self.spec["boost"].prefix),
            self.define("BOOST_LIBRARY_DIR", self.spec["boost"].libs.directories[0]),
            self.define("BOOST_INCLUDE_DIR", self.spec["boost"].headers.directories[0]),
            self.define("BOOST_NO_SYSTEM_PATHS", True),
            self.define("Boost_NO_BOOST_CMAKE", True),
        ]
