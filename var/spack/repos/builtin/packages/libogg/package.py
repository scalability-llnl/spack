# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.build_systems import cmake, generic
from spack.package import *


class Libogg(CMakePackage, AutotoolsPackage, Package):
    """Ogg is a multimedia container format, and the native file and stream
    format for the Xiph.org multimedia codecs."""

    homepage = "https://www.xiph.org/ogg/"
    url = "http://downloads.xiph.org/releases/ogg/libogg-1.3.2.tar.gz"

    license("BSD-3-Clause")

    version("1.3.5", sha256="0eb4b4b9420a0f51db142ba3f9c64b333f826532dc0f48c6410ae51f4799b664")
    version("1.3.4", sha256="fe5670640bd49e828d64d2879c31cb4dde9758681bb664f9bdbf159a01b0c76e")
    version("1.3.2", sha256="e19ee34711d7af328cb26287f4137e70630e7261b17cbe3cd41011d73a654692")

    depends_on("c", type="build")  # generated

    variant("shared", default=True, description="Build shared library", when="build_system=cmake")
    variant(
        "pic",
        default=True,
        description="Produce position-independent code (for shared libs)",
        when="build_system=cmake",
    )

    requires("+pic", when="+shared")

    # Backport a patch that fixes an unsigned typedef problem on macOS:
    # https://github.com/xiph/ogg/pull/64
    patch(
        "https://github.com/xiph/ogg/commit/c8fca6b4a02d695b1ceea39b330d4406001c03ed.patch?full_index=1",
        sha256="0f4d289aecb3d5f7329d51f1a72ab10c04c336b25481a40d6d841120721be485",
        when="@1.3.4 platform=darwin",
    )
    build_system(
        conditional("cmake", when="@1.3.4:"),
        conditional("generic", when="@1.3.2 platform=windows"),
        "autotools",
        default="autotools",
    )


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        base_cmake_args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]

        return base_cmake_args


class GenericBuilder(generic.GenericBuilder):
    phases = ["build", "install"]

    def is_64bit(self):
        return "64" in str(self.pkg.spec.target.family)

    def build(self, spec, prefix):
        if spec.satisfies("%msvc"):
            plat_tools = self.pkg.compiler.msvc_version
        else:
            raise RuntimeError("Package does not support non MSVC compilers on Windows")
        ms_build_args = ["libogg_static.vcxproj", "/p:PlatformToolset=v%s" % plat_tools]
        msbuild(*ms_build_args)

    def install(self, spec, prefix):
        mkdirp(prefix.include.ogg)
        mkdirp(prefix.lib)
        mkdirp(prefix.share)
        install(
            os.path.join(self.pkg.stage.source_path, "include", "ogg", "*.h"), prefix.include.ogg
        )
        plat_prefix = "x64" if self.is_64bit() else "x86"
        install(os.path.join(plat_prefix, "Debug", "*.lib"), prefix.lib)
        install_tree(os.path.join(self.pkg.stage.source_path, "doc"), prefix.share)
