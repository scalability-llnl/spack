# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shlex

from spack.build_systems.cmake import CMakeBuilder
from spack.package import *


class PyBlosc2(PythonPackage):
    """Python wrapper for the C-Blosc2 library."""

    homepage = "https://github.com/Blosc/python-blosc2"
    pypi = "blosc2/blosc2-2.2.8.tar.gz"

    license("BSD-3-Clause")

    version("2.6.2", sha256="8ca29d9aa988b85318bd8a9b707a7a06c8d6604ae1304cae059170437ae4f53a")
    version("2.2.8", sha256="59065aac5e9b01b0e9f3825d8e7f69f64b59bbfab148a47c54e4115f62a97474")
    version("2.0.0", sha256="f19b0b3674f6c825b490f00d8264b0c540c2cdc11ec7e81178d38b83c57790a1")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("python@3.9:3", when="@2.2:", type=("build", "link", "run"))
    depends_on("python@3.8:3", when="@2.0", type=("build", "link", "run"))
    depends_on("py-numpy@1.20.3:", type=("build", "link", "run"))
    depends_on("py-ndindex@1.4:", when="@2.2:", type=("build", "run"))
    depends_on("py-msgpack", type=("build", "run"))
    depends_on("py-py-cpuinfo", when="@2.2:", type=("build", "run"))
    depends_on("c-blosc2", type="link")

    with default_args(type="build"):
        depends_on("py-setuptools")
        depends_on("py-scikit-build")
        depends_on("py-cython")
        depends_on("cmake@3.11:")
        depends_on("ninja")
        depends_on("pkgconfig")

    def setup_build_environment(self, env):
        cmake_args = [*CMakeBuilder.std_args(self), CMakeBuilder.define("USE_SYSTEM_BLOSC2", True)]
        # scikit-build does not want a CMAKE_INSTALL_PREFIX
        cmake_args = [arg for arg in cmake_args if "CMAKE_INSTALL_PREFIX" not in arg]
        env.set("SKBUILD_CONFIGURE_OPTIONS", " ".join(shlex.quote(arg) for arg in cmake_args))
