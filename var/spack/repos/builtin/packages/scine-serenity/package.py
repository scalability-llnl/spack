# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ScineSerenity(CMakePackage):
    """Wrapper around Serenity to make it compatible with Scine"""

    homepage = "https://scine.ethz.ch"
    url = "https://github.com/qcscine/serenity_wrapper/archive/refs/tags/1.0.1.tar.gz"
    git = "https://github.com/qcscine/serenity_wrapper"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.0.1", sha256="e2e5cc265a68ccab05f1bc934b957ca07c4f1c6004e662684023da451da69299")

    depends_on("cxx", type="build")  # generated

    resource(
        name="dev",
        url="https://github.com/qcscine/development-utils/archive/refs/tags/5.0.1.tar.gz",
        sha256="089ca500fc191e04a968ea166d2fe80178b227bc2e6d3926523fa2eee5f6492d",
        placement="_dev",
    )

    variant("python", default=False, description="Build Python extension module")

    depends_on("boost+system+filesystem+program_options cxxstd=17 @1.65.0:")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("scine-core")
    depends_on("scine-utilities")
    depends_on("scine-utilities+python", when="+python", type=("build", "run"))
    depends_on("serenity")

    extends("python", when="+python")

    def patch(self):
        os.rmdir("dev")
        os.rename("_dev", "dev")

        filter_file(
            # Serenity does not install any config or targets file...
            "find_package(serenity QUIET)",
            "find_library(SERENITY_LIBRARY serenity REQUIRED)\n"
            "add_library(serenity INTERFACE IMPORTED)\n"
            "target_link_libraries(serenity INTERFACE ${SERENITY_LIBRARY})\n"
            "target_include_directories(serenity INTERFACE ${SERENITY_INCLUDE_DIR})\n"
            "find_package(OpenMP REQUIRED)\n"
            "target_compile_options(serenity INTERFACE ${OpenMP_CXX_FLAGS})\n",
            "CMakeLists.txt",
            string=True,
        )

    def cmake_args(self):
        return [
            self.define("SCINE_BUILD_TESTS", self.run_tests),
            self.define_from_variant("SCINE_BUILD_PYTHON_BINDINGS", "python"),
            self.define("SCINE_MARCH", ""),
            self.define("serenity_DIR", self.spec["serenity"].prefix.lib.cmake.serenity),
            self.define("SERENITY_INCLUDE_DIR", self.spec["serenity"].prefix.include.serenity),
            self.define("BOOST_ROOT", self.spec["boost"].prefix),
            self.define("BOOST_LIBRARY_DIR", self.spec["boost"].libs.directories[0]),
            self.define("BOOST_INCLUDE_DIR", self.spec["boost"].headers.directories[0]),
            self.define("BOOST_NO_SYSTEM_PATHS", True),
            self.define("Boost_NO_BOOST_CMAKE", True),
        ]
