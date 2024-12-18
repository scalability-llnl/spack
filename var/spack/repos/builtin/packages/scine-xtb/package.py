# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ScineXtb(CMakePackage):
    """Wrapper around xtb to export it into the Scine tool chain."""

    homepage = "https://scine.ethz.ch"
    url = "https://github.com/qcscine/xtb_wrapper/archive/refs/tags/1.0.2.tar.gz"
    git = "https://github.com/qcscine/xtb_wrapper.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.0.2", sha256="9beb1103467f3cfd9ad33beb2f3ec650bc3e6dc7094876774be3cc4e6f210487")

    depends_on("cxx", type="build")  # generated

    resource(
        name="dev",
        url="https://github.com/qcscine/development-utils/archive/refs/tags/5.0.1.tar.gz",
        sha256="089ca500fc191e04a968ea166d2fe80178b227bc2e6d3926523fa2eee5f6492d",
        placement="_dev",
    )

    patch(
        "https://raw.githubusercontent.com/conda-forge/scine-xtb-feedstock/4ac2b70/recipe/patches/pkgconfig.patch",
        level=1,
        sha256="8650abf9dca269f62b60733aabfac0681d9d1cfd721bec728752fb4cbca44452",
    )

    variant("python", default=False, description="Build Python extension module")

    depends_on("boost+system+filesystem+program_options cxxstd=17 @1.65.0:")
    depends_on("eigen@3:")
    depends_on("pkgconfig", type="build")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("scine-core")
    depends_on("scine-utilities")
    depends_on("scine-utilities+python", when="+python", type=("build", "run"))
    depends_on("xtb")

    extends("python", when="+python")

    def patch(self):
        os.rmdir("dev")
        os.rename("_dev", "dev")

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
