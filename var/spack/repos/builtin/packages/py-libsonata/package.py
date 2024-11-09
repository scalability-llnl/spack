# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLibsonata(PythonPackage):
    """SONATA files reader"""

    homepage = "https://github.com/BlueBrain/libsonata"
    git = "https://github.com/BlueBrain/libsonata.git"
    pypi = "libsonata/libsonata-0.1.14.tar.gz"

    maintainers("tristan0x")

    version("master", branch="master")
    version("0.1.25", sha256="b332efa718123ee265263e1583a5998eaa945a13b8a22903873764cf1d8173fa")

    depends_on("cxx", type="build")  # generated

    depends_on("catch2@2.13:", type="test")
    depends_on("cmake@3.16:", type="build")
    depends_on("fmt@7.1:")
    depends_on("hdf5@1.14:")
    depends_on("highfive@2.9:")
    depends_on("nlohmann-json@3.9.1")
    depends_on("py-pybind11@2.11.1:")

    depends_on("py-numpy@1.17.3:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build", when="@0.1:")
    depends_on("py-setuptools-scm@3.4:", type="build", when="@0.1:")

    def patch(self):
        filter_file("-DEXTLIB_FROM_SUBMODULES=ON", "-DEXTLIB_FROM_SUBMODULES=OFF", "setup.py")
