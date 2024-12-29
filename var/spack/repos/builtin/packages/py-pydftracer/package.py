# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydftracer(PythonPackage):
    """A low-level profiler for capture I/O calls from deep learning applications."""

    homepage = "https://github.com/hariharan-devarajan/dlio-profiler.git"
    git = "https://github.com/hariharan-devarajan/dlio-profiler.git"
    maintainers("hariharan-devarajan")

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("1.0.3", tag="v1.0.3", commit="856de0b958a22081d80a9a25bea3f74e2759d9ee")
    version("1.0.2", tag="v1.0.2", commit="8a15f09ff54a909605eda0070689c0b99401db20")
    version("1.0.1", tag="v1.0.1", commit="dc1ce44042e669e6da495f906ca5f8b155c9f155")
    version("1.0.0", tag="v1.0.0", commit="b6df57d81ffb043b468e2bd3e8df9959fdb4af53")

    depends_on("cpp-logger@0.0.4", when="@1.0.0:")
    depends_on("brahma@0.0.5", when="@1.0.0:")
    depends_on("yaml-cpp@0.6.3", when="@1.0.0:")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-pybind11", type=("build", "run"))
    depends_on("ninja", type="build")
    depends_on("cmake@3.12:", type="build")

    def setup_build_environment(self, env):
        env.set("DFTRACER_INSTALL_DIR", self.prefix)
        env.set("DFTRACER_PYTHON_SITE", python_purelib)
        env.set("DFTRACER_BUILD_DEPENDENCIES", "0")
