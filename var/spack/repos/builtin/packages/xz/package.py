# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import re

from spack.build_systems.autotools import AutotoolsBuilder
from spack.build_systems.msbuild import MSBuildBuilder
from spack.package import *


class Xz(MSBuildPackage, AutotoolsPackage, SourceforgePackage):
    """XZ Utils is free general-purpose data compression software with
    high compression ratio. XZ Utils were written for POSIX-like systems,
    but also work on some not-so-POSIX systems. XZ Utils are the successor
    to LZMA Utils."""

    homepage = "https://tukaani.org/xz/"
    sourceforge_mirror_path = "lzmautils/files/xz-5.2.5.tar.bz2"
    list_url = "https://tukaani.org/xz/old.html"

    maintainers("AlexanderRichert-NOAA")

    executables = [r"^xz$"]

    license("GPL-2.0-or-later AND Public-Domain AND LGPL-2.1-or-later", checked_by="tgamblin")

    # NOTE: don't add XZ 5.6 until this compromise is resolved:
    # https://www.openwall.com/lists/oss-security/2024/03/29/4
    version("5.4.6", sha256="913851b274e8e1d31781ec949f1c23e8dbcf0ecf6e73a2436dc21769dd3e6f49")
    version("5.4.5", sha256="8ccf5fff868c006f29522e386fb4c6a1b66463fbca65a4cfc3c4bd596e895e79")
    version("5.4.1", sha256="dd172acb53867a68012f94c17389401b2f274a1aa5ae8f84cbfb8b7e383ea8d3")
    version("5.2.10", sha256="01b71df61521d9da698ce3c33148bff06a131628ff037398c09482f3a26e5408")
    version("5.2.7", sha256="b65f1d0c2708e57716f4dd2216989a73847ac6fdb4168ffceb155767e22b834b")
    version("5.2.6", sha256="13e3402e301b6018f6a71ef0e497f714c6d11e214ae82dab156b81c2a64acb25")
    version("5.2.5", sha256="5117f930900b341493827d63aa910ff5e011e0b994197c3b71c08a20228a42df")
    version("5.2.4", sha256="3313fd2a95f43d88e44264e6b015e7d03053e681860b0d5d3f9baca79c57b7bf")
    version("5.2.3", sha256="fd9ca16de1052aac899ad3495ad20dfa906c27b4a5070102a2ec35ca3a4740c1")
    version("5.2.2", sha256="6ff5f57a4b9167155e35e6da8b529de69270efb2b4cf3fbabf41a4ee793840b5")
    version("5.2.1", sha256="679148f497e0bff2c1adce42dee5a23f746e71321c33ebb0f641a302e30c2a80")
    version("5.2.0", sha256="f7357d7455a1670229b3cca021da71dd5d13b789db62743c20624bdffc9cc4a5")

    depends_on("c", type="build")  # generated

    variant("pic", default=False, description="Compile with position independent code.")

    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )

    # xz-5.2.7/src/liblzma/common/common.h:56 uses attribute __symver__ instead of
    # __asm__(.symver) for newer GCC releases.
    conflicts("%intel", when="@5.2.7", msg="icc does not support attribute __symver__")
    conflicts("platform=windows", when="+pic")  # no pic on Windows
    # prior to 5.2.3, build system is for MinGW only, not currently supported by Spack
    conflicts("platform=windows", when="@:5.2.3")

    build_system(conditional("msbuild", when="platform=windows"), "autotools", default="autotools")

    def flag_handler(self, name, flags):
        if name == "cflags" and "+pic" in self.spec:
            flags.append(self.compiler.cc_pic_flag)
        return (flags, None, None)

    @property
    def libs(self):
        return find_libraries(
            ["liblzma"],
            root=self.prefix,
            recursive=True,
            shared=self.spec.satisfies("libs=shared"),
        )

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"xz \(XZ Utils\) (\S+)", output)
        return match.group(1) if match else None


class AutotoolsBuilder(AutotoolsBuilder):
    def configure_args(self):
        return self.enable_or_disable("libs")

    @run_after("install")
    def darwin_fix(self):
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)


class MSBuildBuilder(MSBuildBuilder):
    @property
    def build_directory(self):
        def get_file_string_number(f):
            s = re.findall(r"\d+$", f)
            return (int(s[0]) if s else -1, f)

        win_dir = os.path.join(super().build_directory, "windows")
        compiler_dirs = []
        with working_dir(win_dir):
            for obj in os.scandir():
                if obj.is_dir():
                    compiler_dirs.append(obj.name)
        newest_compiler = max(compiler_dirs, key=get_file_string_number)
        return os.path.join(win_dir, newest_compiler)

    def is_64bit(self):
        return "64" in str(self.pkg.spec.target.family)

    def msbuild_args(self):
        plat = "x64" if self.is_64bit() else "x86"
        if self.pkg.spec.satisfies("libs=shared,static"):
            f = "xz_win.sln"
        elif self.pkg.spec.satisfies("libs=shared"):
            f = "liblzma_dll.vcxproj"
        else:
            f = "liblzma.vcxproj"
        return [self.define("Configuration", "Release"), self.define("Platform", plat), f]

    def install(self, pkg, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.lib)
            mkdirp(prefix.bin)
            libs_to_find = []
            dlls_to_find = []
            if self.pkg.spec.satisfies("libs=shared"):
                dlls_to_find.append("*.dll")
            if self.pkg.spec.satisfies("libs=static"):
                libs_to_find.append("*.lib")
            for lib in libs_to_find:
                libs_to_install = glob.glob(
                    os.path.join(self.build_directory, "**", lib), recursive=True
                )
                for lib_to_install in libs_to_install:
                    install(lib_to_install, prefix.lib)
            for dll in dlls_to_find:
                dlls_to_install = glob.glob(
                    os.path.join(self.build_directory, "**", dll), recursive=True
                )
                for dll_to_install in dlls_to_install:
                    install(dll_to_install, prefix.bin)

        with working_dir(pkg.stage.source_path):
            install_tree(os.path.join("src", "liblzma", "api"), prefix.include)
