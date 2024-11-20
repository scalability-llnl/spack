# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import autotools, cmake
from spack.package import *


class Gperftools(AutotoolsPackage, CMakePackage):
    """Google's fast malloc/free implementation, especially for
    multi-threaded applications.  Contains tcmalloc, heap-checker,
    heap-profiler, and cpu-profiler.

    """

    homepage = "https://github.com/gperftools/gperftools"
    url = "https://github.com/gperftools/gperftools/releases/download/gperftools-2.7/gperftools-2.7.tar.gz"
    maintainers("albestro", "eschnett", "msimberg", "teonnik")

    license("BSD-3-Clause")

    build_system(conditional("cmake", when="@2.8.1:"), "autotools", default="cmake")

    version("2.16", sha256="f12624af5c5987f2cc830ee534f754c3c5961eec08004c26a8b80de015cf056f")
    version("2.15", sha256="c69fef855628c81ef56f12e3c58f2b7ce1f326c0a1fe783e5cae0b88cbbe9a80")
    version("2.14", sha256="6b561baf304b53d0a25311bd2e29bc993bed76b7c562380949e7cb5e3846b299")
    version("2.13", sha256="4882c5ece69f8691e51ffd6486df7d79dbf43b0c909d84d3c0883e30d27323e7")
    version("2.12", sha256="fb611b56871a3d9c92ab0cc41f9c807e8dfa81a54a4a9de7f30e838756b5c7c6")
    version("2.11", sha256="8ffda10e7c500fea23df182d7adddbf378a203c681515ad913c28a64b87e24dc")
    version("2.10", sha256="83e3bfdd28b8bcf53222c3798d4d395d52dadbbae59e8730c4a6d31a9c3732d8")
    version("2.9.1", sha256="ea566e528605befb830671e359118c2da718f721c27225cbbc93858c7520fee3")
    version("2.8.1", sha256="12f07a8ba447f12a3ae15e6e3a6ad74de35163b787c0c7b76288d7395f2f74e0")
    version("2.7", sha256="1ee8c8699a0eff6b6a203e59b43330536b22bbcbe6448f54c7091e5efb0763c9")
    version("2.4", sha256="982a37226eb42f40714e26b8076815d5ea677a422fb52ff8bfca3704d9c30a2d")
    version("2.3", sha256="093452ad45d639093c144b4ec732a3417e8ee1f3744f2b0f8d45c996223385ce")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("sized_delete", default=False, description="Build sized delete operator")
    variant(
        "dynamic_sized_delete_support",
        default=False,
        description="Try to build run-time switch for sized delete operator",
    )
    variant("debugalloc", default=True, description="Build versions of libs with debugalloc")
    variant(
        "libunwind", default=True, when="platform=linux", description="Enable libunwind linking"
    )

    depends_on("unwind", when="+libunwind")
    depends_on("cmake@3.12:", type="build", when="build_system=cmake")
    # https://github.com/gperftools/gperftools/commit/9dfab2cdce5ec1ebb36e2a20e5031ef49cbe8087
    conflicts("build_system=cmake", when="@2.16:")

    # Linker error: src/base/dynamic_annotations.cc:46: undefined reference to
    # `TCMallocGetenvSafe'
    conflicts("target=ppc64:", when="@2.14")
    conflicts("target=ppc64le:", when="@2.14")

    # the autotools build system creates an explicit list of -L <system dir> flags that end up
    # before the -L <spack dir> flags, which causes the system libunwind to be linked instead of
    # the spack libunwind. This is a workaround to fix that.
    conflicts("+libunwind", when="build_system=autotools")


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        return [
            self.define_from_variant("gperftools_sized_delete", "sized_delete"),
            self.define_from_variant(
                "gperftools_dynamic_sized_delete_support", "dynamic_sized_delete_support"
            ),
            self.define_from_variant("GPERFTOOLS_BUILD_DEBUGALLOC", "debugalloc"),
            self.define_from_variant("gperftools_enable_libunwind", "libunwind"),
            self.define("gperftools_build_benchmark", False),
            self.define("BUILD_TESTING", False),
        ]


class AutotooolsBuilder(autotools.AutotoolsBuilder):
    def configure_args(self):
        return [
            *self.enable_or_disable("sized-delete", variant="sized_delete"),
            *self.enable_or_disable(
                "dynamic-sized-delete-support", variant="dynamic_sized_delete_support"
            ),
            *self.enable_or_disable("debugalloc"),
            *self.enable_or_disable("libunwind"),
        ]
