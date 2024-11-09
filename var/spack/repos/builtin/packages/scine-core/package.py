# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ScineCore(CMakePackage):
    """Core provides the functionality necessary to couple the individual SCINE modules together"""

    homepage = "https://scine.ethz.ch/"
    url = "https://github.com/qcscine/core/archive/refs/tags/4.0.2.tar.gz"
    git = "https://github.com/qcscine/core.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("6.0.0", sha256="6e47e49694002f9d847507c9aacfe53b2befbff5aa380f8860468afdfe880461")
    version("4.0.2", sha256="7181c6f93d71def22f1e0e5767afc7587c04b49abc03516f6926394868e7adc6")

    depends_on("cxx", type="build")  # generated

    resource(
        name="dev",
        url="https://github.com/qcscine/development-utils/archive/refs/tags/5.0.1.tar.gz",
        sha256="089ca500fc191e04a968ea166d2fe80178b227bc2e6d3926523fa2eee5f6492d",
        placement="_dev",
    )

    depends_on("boost+filesystem+program_options cxxstd=17 @1.65.0:")
    depends_on("googletest", type="build")

    def patch(self):
        os.rmdir("dev")
        os.rename("_dev", "dev")

    def cmake_args(self):
        return [
            self.define("SCINE_BUILD_TESTS", self.run_tests),
            self.define("SCINE_MARCH", ""),
            self.define("BOOST_ROOT", self.spec["boost"].prefix),
            self.define("BOOST_LIBRARY_DIR", self.spec["boost"].libs.directories[0]),
            self.define("BOOST_INCLUDE_DIR", self.spec["boost"].headers.directories[0]),
            self.define("BOOST_NO_SYSTEM_PATHS", True),
            self.define("Boost_NO_BOOST_CMAKE", True),
        ]
