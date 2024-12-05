# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Brahma(CMakePackage):
    """Interceptor library for I/O calls using Gotcha"""

    homepage = "https://github.com/hariharan-devarajan/brahma"
    git = "https://github.com/hariharan-devarajan/brahma.git"
    maintainers("hariharan-devarajan")

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("0.0.5", tag="v0.0.5", commit="219198c653cc4add845a644872e7b963a8de0fe2")
    version("0.0.4", tag="v0.0.4", commit="8f41cc885dd8e31a1f134cbbcbaaab7e5d84331e")
    version("0.0.3", tag="v0.0.3", commit="fd201c653e8fa00d4ba6197a56a513f740e3014e")
    version("0.0.2", tag="v0.0.2", commit="4a36d5c08787d41c939fa1b987344b69d9ef97a6")
    version("0.0.1", tag="v0.0.1", commit="15156036f14e36511dfc3f3751dc953540526a2b")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=False, description="Enable MPI support")
    depends_on("cpp-logger@0.0.1", when="@:0.0.1")
    depends_on("cpp-logger@0.0.2", when="@0.0.2:0.0.3")
    depends_on("cpp-logger@0.0.3", when="@0.0.4")
    depends_on("cpp-logger@0.0.4", when="@0.0.5:")
    depends_on("gotcha@1.0.4", when="@:0.0.1")
    depends_on("gotcha@1.0.5", when="@0.0.2:0.0.3")
    depends_on("gotcha@1.0.6", when="@0.0.4")
    depends_on("gotcha@1.0.7", when="@0.0.5:")
    depends_on("catch2@3.0.1:")

    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        prefix = "BRAHMA_" if self.spec.satisfies("@0.0.4:") else ""
        return [self.define_from_variant(f"{prefix}BUILD_WITH_MPI", "mpi")]
