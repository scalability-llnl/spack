# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ScineSparrow(CMakePackage):
    """Sparrow: fast semiempirical quantum chemical calculations.

    When publishing results obtained with Sparrow, please cite
    the corresponding release as archived on Zenodo
    (DOI 10.5281/zenodo.3244105; please use the DOI of the respective
    release).

    In addition, we kindly request you to cite the following article
    when using Sparrow:

    T. Husch, A. C. Vaucher, M. Reiher, "Semiempirical molecular orbital
    models based on the neglect of diatomic differential overlap
    approximation", Int. J. Quantum Chem., 2018, 118, e25799.
    """

    homepage = "https://scine.ethz.ch/download/sparrow"
    url = "https://github.com/qcscine/sparrow/archive/refs/tags/3.1.0.tar.gz"
    git = "https://github.com/qcscine/sparrow.git"

    maintainers("frobnitzem")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("3.1.0", sha256="91412de0f2670a1735c4ca76406db5bea04236eeac0bc1f93ccfe18104aa7ce4")
    version("3.0.0", sha256="70636871694c9363ae3fb2df5050bddb22667b71d875d5a7e9afd872f6a2b65d")

    depends_on("cxx", type="build")  # generated

    resource(
        name="dev",
        url="https://github.com/qcscine/development-utils/archive/refs/tags/5.0.1.tar.gz",
        sha256="089ca500fc191e04a968ea166d2fe80178b227bc2e6d3926523fa2eee5f6492d",
        placement="_dev",
    )

    variant("python", default=False, description="Build Python extension module")

    depends_on("boost+filesystem+program_options cxxstd=17 @1.65.0:")
    depends_on("cereal")
    depends_on("eigen@3.3.2:")
    depends_on("googletest", type="build")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("scine-core")
    depends_on("scine-utilities")
    depends_on("scine-utilities+python", when="+python", type=("build", "run"))
    depends_on("yaml-cpp")

    extends("python", when="+python")

    def patch(self):
        os.rmdir("dev")
        os.rename("_dev", "dev")

        if self.spec.satisfies("platform=darwin"):
            filter_file(
                r"SparrowApp PROPERTIES OUTPUT_NAME sparrow",
                'SparrowApp PROPERTIES OUTPUT_NAME sparrow SUFFIX ".exe"',
                "src/Sparrow/CMakeLists.txt",
            )

        filter_file(
            "#include <iostream>",
            "#include <iostream>\n#include <fstream>",
            "src/Sparrow/Sparrow/Implementations/Dftb/Utils/SkfParser.cpp",
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

    # Adapted from ddd in MacPorts: cmake will build the executable
    # "sparrow" right next to the copy of the source directory "Sparrow".
    # As HFS+ is case-insensitive by default this will loosely FAIL.
    # Mitigate this by building/installing 'sparrowexe'
    # on Darwin and fixing up post install.
    @run_after("install")
    def _rename_exe_on_darwin(self):
        if self.spec.satisfies("platform=darwin"):
            with working_dir(self.prefix.bin):
                os.rename("sparrow.exe", "sparrow")
