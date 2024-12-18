# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XtensorPython(CMakePackage):
    """Python bindings for the xtensor C++ multi-dimensional array library"""

    homepage = "https://xtensor-python.readthedocs.io"
    url = "https://github.com/QuantStack/xtensor-python/archive/0.17.0.tar.gz"
    git = "https://github.com/QuantStack/xtensor-python.git"

    maintainers("ax3l")

    license("BSD-3-Clause")

    version("develop", branch="master")
    version("0.23.1", sha256="450b25f5c739df174b2a50774b89e68b23535fdc37cb55bd542ffdb7c78991ab")
    version("0.17.0", sha256="30f2e8c99376e38f942d62c0d2959bc1e52a562a4f8cc5e27ddc4d572a25e34c")

    depends_on("cxx", type="build")  # generated

    depends_on("xtensor", when="@develop")
    depends_on("xtensor@0.20.6:0.20", when="@0.23.1")
    depends_on("xtensor@0.15.1:0.15", when="@0.17.0")
    depends_on("xtl", when="@develop")
    depends_on("xtl@0.6.4:0.6", when="@0.23.1")
    depends_on("xtl@0.4.0:0.4", when="@0.17.0")
    depends_on("py-pybind11@2.2.1:2.2")

    depends_on("py-numpy")
    depends_on("python", type=("build", "link", "run"))

    extends("python")
