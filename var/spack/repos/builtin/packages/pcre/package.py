# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.autotools
import spack.build_systems.cmake
from spack.package import *


class Pcre(AutotoolsPackage, CMakePackage):
    """The PCRE package contains Perl Compatible Regular Expression
    libraries. These are useful for implementing regular expression
    pattern matching using the same syntax and semantics as Perl 5."""

    homepage = "https://www.pcre.org"
    url = "https://sourceforge.net/projects/pcre/files/pcre/8.42/pcre-8.42.tar.bz2"

    license("BSD-3-Clause")

    version("8.45", sha256="4dae6fdcd2bb0bb6c37b5f97c33c2be954da743985369cddac3546e3218bffb8")
    version("8.44", sha256="19108658b23b3ec5058edc9f66ac545ea19f9537234be1ec62b714c84399366d")
    version("8.43", sha256="91e762520003013834ac1adb4a938d53b22a216341c061b0cf05603b290faf6b")
    version("8.42", sha256="2cd04b7c887808be030254e8d77de11d3fe9d4505c39d4b15d2664ffe8bf9301")
    version("8.41", sha256="e62c7eac5ae7c0e7286db61ff82912e1c0b7a0c13706616e94a7dd729321b530")
    version("8.40", sha256="00e27a29ead4267e3de8111fcaa59b132d0533cdfdbdddf4b0604279acbcf4f4")
    version("8.39", sha256="b858099f82483031ee02092711689e7245586ada49e534a06e678b8ea9549e8b")
    version("8.38", sha256="b9e02d36e23024d6c02a2e5b25204b3a4fa6ade43e0a5f869f254f49535079df")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    maintainers("drkennetz")
    patch("intel.patch", when="@8.38")

    build_system("autotools", "cmake", default="autotools")

    variant("jit", default=False, description="Enable JIT support.")

    variant("multibyte", default=True, description="Enable support for 16 and 32 bit characters.")

    variant(
        "utf",
        default=True,
        description="Enable support for UTF-8/16/32, " "incompatible with EBCDIC.",
    )

    variant("shared", default=True, description="Build shared libraries")
    variant("static", default=True, description="Build static libraries")
    conflicts("-shared -static", msg="Must build one of shared and static")
    conflicts(
        "+shared +static",
        when="build_system=cmake",
        msg="CMake can only build either shared or static",
    )

    variant("pic", default=True, description="Enable position-independent code (PIC)")
    requires("+pic", when="+shared build_system=autotools")

    with when("build_system=cmake"):
        depends_on("zlib")
        depends_on("bzip2")


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []

        args.extend(self.enable_or_disable("shared"))
        args.extend(self.enable_or_disable("static"))
        args.extend(self.with_or_without("pic"))

        args.extend(self.enable_or_disable("jit"))

        args.extend(self.enable_or_disable("pcre16", variant="multibyte"))
        args.extend(self.enable_or_disable("pcre32", variant="multibyte"))

        args.extend(self.enable_or_disable("utf"))
        args.extend(self.enable_or_disable("unicode-properties", variant="utf"))

        return args


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        args = []

        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("BUILD_STATIC_LIBS", "static"))
        args.append(self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"))

        args.append(self.define_from_variant("PCRE_SUPPORT_JIT", "jit"))

        args.append(self.define_from_variant("PCRE_BUILD_PCRE16", "multibyte"))
        args.append(self.define_from_variant("PCRE_BUILD_PCRE32", "multibyte"))

        args.append(self.define_from_variant("PCRE_SUPPORT_UTF", "utf"))
        args.append(self.define_from_variant("PCRE_SUPPORT_UNICODE_PROPERTIES", "utf"))

        return args
