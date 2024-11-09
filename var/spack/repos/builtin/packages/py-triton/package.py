# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTriton(PythonPackage):
    """A language and compiler for custom Deep Learning operations."""

    homepage = "https://github.com/openai/triton"
    url = "https://github.com/openai/triton/archive/refs/tags/v2.1.0.tar.gz"
    git = "https://github.com/openai/triton.git"

    license("MIT")

    version("main", branch="main")
    version("2.1.0", sha256="4338ca0e80a059aec2671f02bfc9320119b051f378449cf5f56a1273597a3d99")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@40.8:", type="build")
    depends_on("cmake@3.18:", type="build")
    depends_on("py-filelock", type=("build", "run"))
    depends_on("zlib-api", type="link")
    conflicts("^openssl@3.3.0")

    def setup_build_environment(self, env):
        """Set environment variables used to control the build"""
        if self.spec.satisfies("%clang"):
            env.set("TRITON_BUILD_WITH_CLANG_LLD", "True")

    build_directory = "python"
