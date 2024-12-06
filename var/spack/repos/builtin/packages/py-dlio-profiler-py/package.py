# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDlioProfilerPy(PythonPackage):
    """A low-level profiler for capture I/O calls from deep learning applications."""

    homepage = "https://github.com/hariharan-devarajan/dlio-profiler.git"
    git = "https://github.com/hariharan-devarajan/dlio-profiler.git"
    maintainers("hariharan-devarajan")

    license("MIT")

    version(
        "0.0.7", tag="v0.0.7", commit="e47ec476b58e14157b807cbadb4187bd4fe811d9", deprecated=True
    )
    version(
        "0.0.6", tag="v0.0.6", commit="3be111c973883387418ad96f63a18de63555c540", deprecated=True
    )
    version(
        "0.0.5", tag="v0.0.5", commit="08f1a43c67c8dbb458d547020674c86118c9742e", deprecated=True
    )
    version(
        "0.0.4", tag="v0.0.4", commit="f9ba207f4c3e3789eb7759653a94013e6b76c91c", deprecated=True
    )
    version(
        "0.0.3", tag="v0.0.3", commit="531f4475cf03312e121c78bf644445882b51ad57", deprecated=True
    )
    version(
        "0.0.2", tag="v0.0.2", commit="b72144abf1499e03d1db87ef51e780633e9e9533", deprecated=True
    )
    version(
        "0.0.1", tag="v0.0.1", commit="28affe716211315dd6936ddc8e25ce6c43cdf491", deprecated=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cpp-logger@0.0.1", when="@:0.0.1")
    depends_on("cpp-logger@0.0.2", when="@0.0.2")
    depends_on("cpp-logger@0.0.3", when="@0.0.3:0.0.5")
    depends_on("cpp-logger@0.0.4", when="@0.0.6:")
    depends_on("brahma@0.0.1", when="@:0.0.1")
    depends_on("brahma@0.0.2", when="@0.0.2")
    depends_on("brahma@0.0.3", when="@0.0.3:0.0.5")
    depends_on("brahma@0.0.5", when="@0.0.6:")
    depends_on("yaml-cpp@0.6.3", when="@0.0.2:")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-pybind11", type=("build", "run"))
    depends_on("ninja", type="build")
    depends_on("cmake@3.12:", type="build")

    def setup_build_environment(self, env):
        if self.spec.satisfies("@0.0.6:"):
            env.set("DLIO_PROFILER_INSTALL_DIR", self.prefix)
            env.set("DLIO_PROFILER_PYTHON_SITE", python_purelib)
        else:
            env.set("DLIO_PROFILER_DIR", self.prefix)
            env.set("DLIO_PYTHON_SITE", python_purelib)
        env.set("DLIO_BUILD_DEPENDENCIES", "0")
