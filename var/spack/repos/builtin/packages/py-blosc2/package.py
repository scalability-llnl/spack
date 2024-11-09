# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBlosc2(PythonPackage):
    """Python wrapper for the C-Blosc2 library."""

    homepage = "https://github.com/Blosc/python-blosc2"
    pypi = "blosc2/blosc2-2.2.8.tar.gz"

    license("BSD-3-Clause")

    version("2.6.2", sha256="8ca29d9aa988b85318bd8a9b707a7a06c8d6604ae1304cae059170437ae4f53a")
    version("2.2.8", sha256="59065aac5e9b01b0e9f3825d8e7f69f64b59bbfab148a47c54e4115f62a97474")
    version("2.0.0", sha256="f19b0b3674f6c825b490f00d8264b0c540c2cdc11ec7e81178d38b83c57790a1")

    depends_on("c", type="build")  # generated

    depends_on("python@3.9:3", when="@2.2:", type=("build", "link", "run"))
    depends_on("python@3.8:3", when="@2.0", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-scikit-build", type="build")
    depends_on("py-cython", type="build")
    depends_on("cmake@3.11:", type="build")
    depends_on("ninja", type="build")
    depends_on("py-numpy@1.20.3:", type=("build", "link", "run"))
    depends_on("py-ndindex@1.4:", when="@2.2:", type=("build", "run"))
    depends_on("py-msgpack", type=("build", "run"))
    depends_on("py-py-cpuinfo", when="@2.2:", type=("build", "run"))
