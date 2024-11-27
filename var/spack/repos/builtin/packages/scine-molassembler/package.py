# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ScineMolassembler(CMakePackage):
    """Chemoinformatics toolkit with support for inorganic molecules."""

    homepage = "https://scine.ethz.ch/download/molassembler"
    url = "https://github.com/qcscine/molassembler/archive/refs/tags/1.2.1.tar.gz"
    git = "https://github.com/qcscine/molassembler.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.2.1", sha256="c9fea41d383b7f54cf8a3ed4dabebe9e942fe3ef5b47895e3533e8ce42dacd38")

    depends_on("cxx", type="build")  # generated

    resource(
        name="dev",
        url="https://github.com/qcscine/development-utils/archive/refs/tags/5.0.1.tar.gz",
        sha256="089ca500fc191e04a968ea166d2fe80178b227bc2e6d3926523fa2eee5f6492d",
        placement="_dev",
    )

    resource(
        name="nauty-finder",
        url="https://raw.githubusercontent.com/conda-forge/scine-molassembler-feedstock/0aa909d/recipe/cmake/Findnauty.cmake",
        sha256="0746e8a1e35687687866e82797ceb848d941a0c232ed5daa63689476b557e18e",
        destination="cmake",
        expand=False,
    )

    # resource(
    #     name="ringdecomposerlib-finder",
    #     url="https://raw.githubusercontent.com/conda-forge/scine-molassembler-feedstock/0aa909d/recipe/cmake/FindRingDecomposerLib.cmake",
    #     sha256="5ecfbccf48a66d8477011aa576181b56d725f1716cca5a268683e586d761a3ec",
    #     destination="cmake",
    #     expand=False,
    # )

    patch(
        "https://raw.githubusercontent.com/conda-forge/scine-molassembler-feedstock/0aa909d/recipe/patches/nlohmann_json.patch",
        level=1,
        sha256="a9afcc42b264620ee24505c1857b8493c2fb632a1d155362ba4519814922a6af",
    )

    patch(
        "https://raw.githubusercontent.com/conda-forge/scine-molassembler-feedstock/0aa909d/recipe/patches/no_cfenv.patch",
        level=1,
        sha256="4d746ebd3567d7209200614613861995b999e65e7e26fc0338184fffa0cb3fb7",
        when="platform=darwin",
    )

    variant("python", default=False, description="Build Python extension module")

    depends_on("boost+system+filesystem+program_options cxxstd=17 @1.65.0:")
    depends_on("eigen@3:")
    depends_on("googletest", type="build")
    depends_on("nauty")
    depends_on("nlohmann-json", type="build")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-pybind11@2.6.2:", when="+python", type="build")
    # depends_on("ringdecomposerlib")
    depends_on("scine-core")
    depends_on("scine-utilities")
    depends_on("scine-utilities+python", when="+python", type=("build", "run"))

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
            self.define("BUILD_SHARED_LIBS", True),
            self.define("SCINE_BUILD_TESTS", self.run_tests),
            self.define("SCINE_BUILD_PYTHON_BINDINGS", "+python" in self.spec),
            self.define("SCINE_MARCH", ""),
            self.define("BOOST_ROOT", self.spec["boost"].prefix),
            self.define("BOOST_LIBRARY_DIR", self.spec["boost"].libs.directories[0]),
            self.define("BOOST_INCLUDE_DIR", self.spec["boost"].headers.directories[0]),
            self.define("BOOST_NO_SYSTEM_PATHS", True),
            self.define("Boost_NO_BOOST_CMAKE", True),
        ]
