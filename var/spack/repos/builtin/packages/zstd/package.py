# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.build_systems.cmake import CMakeBuilder
from spack.build_systems.makefile import MakefileBuilder
from spack.package import *


class Zstd(CMakePackage, MakefilePackage):
    """Zstandard, or zstd as short version, is a fast lossless compression
    algorithm, targeting real-time compression scenarios at zlib-level and
    better compression ratios."""

    homepage = "https://facebook.github.io/zstd/"
    url = "https://github.com/facebook/zstd/archive/v1.4.3.tar.gz"
    git = "https://github.com/facebook/zstd.git"

    maintainers("haampie")

    license("BSD-3-Clause OR GPL-2.0-or-later")

    version("develop", branch="dev")
    version("1.5.6", sha256="30f35f71c1203369dc979ecde0400ffea93c27391bfd2ac5a9715d2173d92ff7")
    version("1.5.5", sha256="98e9c3d949d1b924e28e01eccb7deed865eefebf25c2f21c702e5cd5b63b85e1")
    version("1.5.4", sha256="35ad983197f8f8eb0c963877bf8be50490a0b3df54b4edeb8399ba8a8b2f60a4")
    version("1.5.2", sha256="f7de13462f7a82c29ab865820149e778cbfe01087b3a55b5332707abf9db4a6e")
    version("1.5.0", sha256="0d9ade222c64e912d6957b11c923e214e2e010a18f39bec102f572e693ba2867")
    version("1.4.9", sha256="acf714d98e3db7b876e5b540cbf6dee298f60eb3c0723104f6d3f065cd60d6a8")
    version("1.4.8", sha256="f176f0626cb797022fbf257c3c644d71c1c747bb74c32201f9203654da35e9fa")
    version("1.4.7", sha256="085500c8d0b9c83afbc1dc0d8b4889336ad019eba930c5d6a9c6c86c20c769c8")
    version("1.4.5", sha256="734d1f565c42f691f8420c8d06783ad818060fc390dee43ae0a89f86d0a4f8c2")
    version("1.4.4", sha256="a364f5162c7d1a455cc915e8e3cf5f4bd8b75d09bc0f53965b0c9ca1383c52c8")
    version("1.4.3", sha256="5eda3502ecc285c3c92ee0cc8cd002234dee39d539b3f692997a0e80de1d33de")
    version("1.4.2", sha256="7a6e1dad34054b35e2e847eb3289be8820a5d378228802239852f913c6dcf6a7")
    version("1.4.0", sha256="63be339137d2b683c6d19a9e34f4fb684790e864fee13c7dd40e197a64c705c1")
    version("1.3.8", sha256="90d902a1282cc4e197a8023b6d6e8d331c1fd1dfe60f7f8e4ee9da40da886dc3")
    version("1.3.0", sha256="0fdba643b438b7cbce700dcc0e7b3e3da6d829088c63757a5984930e2f70b348")
    version("1.1.2", sha256="980b8febb0118e22f6ed70d23b5b3e600995dbf7489c1f6d6122c1411cdda8d8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("programs", default=False, description="Build executables")
    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )
    variant(
        "compression",
        when="+programs",
        values=any_combination_of("zlib", "lz4", "lzma"),
        description="Enable support for additional compression methods in programs",
    )

    depends_on("cmake@3.5:", type="build", when="build_system=cmake @1.5.6:")

    depends_on("zlib-api", when="compression=zlib")
    depends_on("lz4", when="compression=lz4")
    depends_on("xz", when="compression=lzma")

    # +programs builds vendored xxhash, which uses unsupported builtins
    # (last tested: nvhpc@22.3)
    conflicts("+programs %nvhpc")

    conflicts("platform=windows", when="@1.5.6")

    build_system("cmake", "makefile", default="makefile")


class CMakeBuilder(CMakeBuilder):
    @property
    def root_cmakelists_dir(self):
        return os.path.join(super().root_cmakelists_dir, "build", "cmake")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define_from_variant("ZSTD_BUILD_PROGRAMS", "programs"))
        args.extend(
            [
                self.define("ZSTD_BUILD_STATIC", self.spec.satisfies("libs=static")),
                self.define("ZSTD_BUILD_SHARED", self.spec.satisfies("libs=shared")),
            ]
        )
        if "compression=zlib" in spec:
            args.append(self.define("ZSTD_ZLIB_SUPPORT", True))
        if "compression=lzma" in spec:
            args.append(self.define("ZSTD_LZMA_SUPPORT", True))
        if "compression=lz4" in spec:
            args.append(self.define("ZSTD_LZ4_SUPPORT", True))
        return args


class MakefileBuilder(MakefileBuilder):
    def build(self, pkg, spec, prefix):
        pass

    def install(self, pkg, spec, prefix):
        args = ["VERBOSE=1", "PREFIX=" + prefix]

        # Tested %nvhpc@22.3. No support for -MP
        if "%nvhpc" in self.spec:
            args.append("DEPFLAGS=-MT $@ -MMD -MF")
        # library targets
        lib_args = ["-C", "lib"] + args + ["install-pc", "install-includes"]
        if "libs=shared" in spec:
            lib_args.append("install-shared")
        if "libs=static" in spec:
            lib_args.append("install-static")

        # install the library
        make(*lib_args)
        # install the programs
        if "+programs" in spec:
            programs_args = ["-C", "programs"] + args
            # additional compression programs have to be turned off, otherwise the
            # makefile will detect them.
            if "compression=zlib" not in spec:
                programs_args.append("HAVE_ZLIB=0")
            if "compression=lzma" not in spec:
                programs_args.append("HAVE_LZMA=0")
            if "compression=lz4" not in spec:
                programs_args.append("HAVE_LZ4=0")
            programs_args.append("install")
            make(*programs_args)
