# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ScineDatabase(CMakePackage):
    """The SCINE database module is a database wrapper for a MongoDB encoding reaction networks."""

    homepage = "https://scine.ethz.ch/"
    url = "https://github.com/qcscine/database/archive/refs/tags/1.1.0.tar.gz"
    git = "https://github.com/qcscine/database.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.1.0", sha256="a9144631dfb90e06f6924cf58fc5db13719cf8577fcd3bbf788a135060a70c18")

    depends_on("cxx", type="build")  # generated

    resource(
        name="dev",
        url="https://github.com/qcscine/development-utils/archive/refs/tags/5.0.1.tar.gz",
        sha256="089ca500fc191e04a968ea166d2fe80178b227bc2e6d3926523fa2eee5f6492d",
        placement="_dev",
    )

    variant("python", default=False, description="Build Python extension module")

    depends_on("eigen@3:")
    depends_on("googletest", type="build")
    depends_on("mongo-cxx-driver@3.2.1:")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-pybind11", when="+python", type="build")
    depends_on("scine-utilities@5:")
    depends_on("scine-utilities+python", when="+python")

    extends("python", when="+python")

    def patch(self):
        os.rmdir("dev")
        os.rename("_dev", "dev")

        filter_file(
            "#include <mongocxx/collection.hpp>",
            "#include <mongocxx/collection.hpp>\n#include <mongocxx/pipeline.hpp>",
            "src/Database/Database/Collection.cpp",
        )

    def cmake_args(self):
        return [
            self.define("SCINE_BUILD_TESTS", self.run_tests),
            self.define("SCINE_BUILD_PYTHON_BINDINGS", "+python" in self.spec),
            self.define("SCINE_MARCH", ""),
        ]
