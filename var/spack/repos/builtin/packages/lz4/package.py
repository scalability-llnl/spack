# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.build_systems.cmake import CMakeBuilder
from spack.build_systems.makefile import MakefileBuilder
from spack.package import *


class Lz4(CMakePackage, MakefilePackage):
    """LZ4 is lossless compression algorithm, providing compression speed
    at 400 MB/s per core, scalable with multi-cores CPU. It also features
    an extremely fast decoder, with speed in multiple GB/s per core,
    typically reaching RAM speed limits on multi-core systems."""

    homepage = "https://lz4.github.io/lz4/"
    url = "https://github.com/lz4/lz4/archive/v1.9.2.tar.gz"

    maintainers("AlexanderRichert-NOAA")

    # liblz4 is BSD-2-clause; programs, manpages, and everything else are GPL2
    license("BSD-2-Clause AND GPL-2.0-only", checked_by="tgamblin")

    version("1.10.0", sha256="537512904744b35e232912055ccf8ec66d768639ff3abe5788d90d792ec5f48b")
    version("1.9.4", sha256="0b0e3aa07c8c063ddf40b082bdf7e37a1562bda40a0ff5272957f3e987e0e54b")
    version("1.9.3", sha256="030644df4611007ff7dc962d981f390361e6c97a34e5cbc393ddfbe019ffe2c1")
    version("1.9.2", sha256="658ba6191fa44c92280d4aa2c271b0f4fbc0e34d249578dd05e50e76d0e5efcc")
    version("1.9.0", sha256="f8b6d5662fa534bd61227d313535721ae41a68c9d84058b7b7d86e143572dcfb")
    version("1.8.3", sha256="33af5936ac06536805f9745e0b6d61da606a1f8b4cc5c04dd3cbaca3b9b4fc43")
    version("1.8.1.2", sha256="12f3a9e776a923275b2dc78ae138b4967ad6280863b77ff733028ce89b8123f9")
    version("1.7.5", sha256="0190cacd63022ccb86f44fa5041dc6c3804407ad61550ca21c382827319e7e7e")
    version("1.3.1", sha256="9d4d00614d6b9dec3114b33d1224b6262b99ace24434c53487a0c8fd0b18cfed")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("valgrind", type="test")

    build_system("cmake", "makefile", default="makefile")
    parallel = False if sys.platform == "win32" else True
    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )
    variant("pic", default=True, description="Enable position-independent code (PIC)")

    def url_for_version(self, version):
        url = "https://github.com/lz4/lz4/archive"

        if version > Version("1.3.1"):
            return "{0}/v{1}.tar.gz".format(url, version)
        else:
            return "{0}/r{1}.tar.gz".format(url, version.joined)

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc@:20.11"):
            filter_file("-fvisibility=hidden", "", "Makefile")
            filter_file("-fvisibility=hidden", "", "lib/Makefile")
            filter_file("-pedantic", "", "Makefile")


class CMakeBuilder(CMakeBuilder):
    @property
    def root_cmakelists_dir(self):
        return os.path.join(super().root_cmakelists_dir, "build", "cmake")

    def cmake_args(self):
        args = [self.define("CMAKE_POLICY_DEFAULT_CMP0042", "NEW")]
        # # no pic on windows
        if self.spec.satisfies("platform=windows"):
            args.append(self.define("LZ4_POSITION_INDEPENDENT_LIB", False))
        args.append(
            self.define("BUILD_SHARED_LIBS", True if self.spec.satisfies("libs=shared") else False)
        )
        args.append(
            self.define("BUILD_STATIC_LIBS", True if self.spec.satisfies("libs=static") else False)
        )
        args.append(self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"))
        return args


class MakefileBuilder(MakefileBuilder):
    def setup_build_environment(self, env):
        if self.spec.satisfies("+pic"):
            env.set("CFLAGS", self.pkg.compiler.cc_pic_flag)

    def build(self, pkg, spec, prefix):
        par = True
        if spec.compiler.name == "nvhpc":
            # relocation error when building shared and dynamic libs in
            # parallel
            par = False

        if sys.platform != "darwin":
            make("MOREFLAGS=-lrt", parallel=par)  # fixes make error on CentOS6
        else:
            make(parallel=par)

    def install(self, pkg, spec, prefix):
        make(
            "install",
            "PREFIX={0}".format(prefix),
            "BUILD_SHARED={0}".format("yes" if self.spec.satisfies("libs=shared") else "no"),
            "BUILD_STATIC={0}".format("yes" if self.spec.satisfies("libs=static") else "no"),
        )

    @run_after("install", when="platform=darwin")
    def darwin_fix(self):
        fix_darwin_install_name(self.prefix.lib)
