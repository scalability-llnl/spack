# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Sparrow(CMakePackage):
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

    homepage = "https://scine.ethz.ch/"
    url = "https://github.com/qcscine/sparrow/archive/refs/tags/3.0.0.tar.gz"

    maintainers("frobnitzem")

    version(
        "3.0.0",
        sha256="70636871694c9363ae3fb2df5050bddb22667b71d875d5a7e9afd872f6a2b65d",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    resource(
        name="dev",
        url="https://github.com/qcscine/development-utils/archive/refs/tags/4.0.0.tar.gz",
        sha256="54002c2082b6bb75672ec66bf9cf3935bbdf6b085ed9b4d7174cbdedb7c2275d",
        destination="deps",
        placement="dev",
    )

    depends_on("eigen@3.3.2:")
    depends_on("boost+filesystem+program_options cxxstd=17 @1.65.0:")
    depends_on("py-pybind11@2.6.2")
    depends_on("py-pip", type="build")
    depends_on("yaml-cpp")
    depends_on("cereal")
    depends_on("googletest")

    def patch(self):
        os.rmdir("dev")
        os.rename("deps/dev", "dev")
        if self.spec.satisfies("platform=darwin"):
            filter_file(
                r"SparrowApp PROPERTIES OUTPUT_NAME sparrow",
                'SparrowApp PROPERTIES OUTPUT_NAME sparrow SUFFIX ".exe"',
                "src/Sparrow/CMakeLists.txt",
            )
        filter_file(
            r"MAKE_CXX_STANDARD 14 PARENT_SCOPE",
            "MAKE_CXX_STANDARD 17 PARENT_SCOPE",
            "dev/cmake/ComponentSetup.cmake",
        )

    def cmake_args(self):
        args = [
            self.define("SCINE_BUILD_PYTHON_BINDINGS", True),
            self.define("SCINE_BUILD_TESTS", self.run_tests),
        ]

        return args

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
