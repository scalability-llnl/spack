# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Szx(CMakePackage, AutotoolsPackage, CudaPackage):
    """An ultra fast error bounded compressor for scientific datasets"""

    homepage = "https://github.com/szcompressor/szx"
    url = "https://github.com/szcompressor/SZx/archive/refs/tags/1.1.1.tar.gz"
    git = "https://github.com/szcompressor/szx"

    maintainers = ["robertu94"]

    version("main", branch="main")
    version("1.1.1", commit="b1609dde7702135b647fb92f91833fc84de2492e")
    version("1.1.0", commit="194a9dc91ee8c46632f79de3c87a63ec29c52b26")

    depends_on("cxx", type="build")  # generated
    build_system(
        conditional("cmake", when="@1.1.1:"),
        conditional("autotools", when="@:1.1.0"),
        default="cmake",
    )

    variant("cli", default=True, description="install the CLI", when="@1.1.1:")
    variant("examples", default=False, description="install the examples", when="@1.1.1:")
    conflicts("+cuda", when="@:1.1.0")

    with when("build_system=autotools"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")

    class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
        force_autoreconf = True

        def configure_args(self):
            args = ["--enable-openmp", "--enable-fortran"]
            return args

    class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
        def cmake_args(self):
            args = [
                self.define_from_variant("SZx_INSTALL_CLI", "cli"),
                self.define_from_variant("SZx_INSTALL_EXAMPLES", "examples"),
                self.define_from_variant("SZx_BUILD_CUDA", "cuda"),
            ]
            return args
