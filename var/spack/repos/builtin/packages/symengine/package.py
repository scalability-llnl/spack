# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Symengine(CMakePackage):
    """SymEngine is a fast symbolic manipulation library, written in C++."""

    homepage = "https://symengine.org"
    url = "https://github.com/symengine/symengine/archive/v0.2.0.tar.gz"
    git = "https://github.com/symengine/symengine.git"
    maintainers("HaoZeke", "jppelteret")

    license("MIT")

    version("master", branch="master")
    version("0.9.0", sha256="dcf174ac708ed2acea46691f6e78b9eb946d8a2ba62f75e87cf3bf4f0d651724")
    version("0.8.1", sha256="41eb6ae6901c09e53d7f61f0758f9201e81fc534bfeecd4b2bd4b4e6f6768693")
    version("0.7.0", sha256="8b865bb72b71539d9cd2488a0468c6c3ea90cc606062a7880c3ff5af6abd74b1")
    version("0.6.0", sha256="4d2caa86c03eaaa8ed004084d02f87b5c51b6229f8ba70d161227e22d6302f0a")
    version("0.5.0", sha256="5d02002f00d16a0928d1056e6ecb8f34fd59f3bfd8ed0009a55700334dbae29b")
    version("0.4.0", sha256="dd755901a9e2a49e53ba3bbe3f565f94265af05299e57a7b592186dd35916a1b")
    version("0.3.0", sha256="591463cb9e741d59f6dfd39a7943e3865d3afe9eac47d1a9cbf5ca74b9c49476")
    version("0.2.0", sha256="64d050b0b9decd12bf4ea3b7d18d3904dd7cb8baaae9fbac1b8068e3c59709be")
    version("0.1.0", sha256="daba3ba0ae91983a772f66bf755b1953c354fe6dc353588b23705d9a79b011fc")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "boostmp", default=False, description="Compile with Boost multi-precision integer library"
    )
    variant("flint", default=False, description="Compile with Flint integer library")
    variant("llvm", default=False, description="Compile with LLVM JIT compiler support")
    variant("mpc", default=True, description="Compile with MPC library")
    variant("mpfr", default=True, description="Compile with MPFR library")
    variant("openmp", default=False, description="Enable OpenMP support")
    variant("piranha", default=False, description="Compile with Piranha integer library")
    variant("thread_safe", default=True, description="Enable thread safety option")
    variant("shared", default=True, description="Enables the build of shared libraries")
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )

    # NOTE: mpir is a drop-in replacement for gmp
    # NOTE: [mpc,mpfr,flint,piranha] could also be built against mpir
    depends_on("boost", when="+boostmp")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="+boostmp")
    depends_on("cereal", when="@0.9:")
    depends_on("gmp", when="~boostmp")
    depends_on("llvm", when="+llvm")
    depends_on("mpc", when="+mpc~boostmp")
    depends_on("mpfr", when="+mpfr~boostmp")
    depends_on("flint", when="+flint~boostmp")
    depends_on("piranha", when="+piranha~flint~boostmp")

    def cmake_args(self):
        spec = self.spec
        options = []

        # See https://github.com/symengine/symengine/blob/master/README.md
        # for build options
        options.extend(
            [
                "-DWITH_SYMENGINE_RCP:BOOL=ON",
                "-DWITH_SYMENGINE_THREAD_SAFE:BOOL=%s"
                % ("ON" if ("+thread_safe" or "+openmp") in spec else "OFF"),
                self.define("BUILD_TESTS", self.run_tests),
                "-DBUILD_BENCHMARKS:BOOL=ON",
                self.define_from_variant("WITH_LLVM", "llvm"),
                self.define_from_variant("WITH_OPENMP", "openmp"),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            ]
        )

        if sys.platform == "darwin":
            options.extend(["-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=on"])

        # The use of the Cereal serialization library is a hard dependency
        if spec.satisfies("@0.9:"):
            options.extend(["-DWITH_SYSTEM_CEREAL:BOOL=on"])

        if "+boostmp" in spec:
            options.extend(
                [
                    "-DINTEGER_CLASS:STRING=boostmp",
                    "-DBoost_INCLUDE_DIR=%s" % spec["boost"].prefix.include,
                    "-DWITH_MPC:BOOL=OFF",
                    "-DWITH_MPFR:BOOL=OFF",
                ]
            )
        else:
            options.extend(
                [
                    self.define_from_variant("WITH_MPC", "mpc"),
                    self.define_from_variant("WITH_MPFR", "mpfr"),
                ]
            )
            if "+flint" in spec:
                options.extend(["-DWITH_FLINT:BOOL=ON", "-DINTEGER_CLASS:STRING=flint"])
            elif "+piranha" in spec:
                options.extend(["-DWITH_PIRANHA:BOOL=ON", "-DINTEGER_CLASS:STRING=piranha"])
            else:
                options.extend(["-DINTEGER_CLASS:STRING=gmp"])

        return options
