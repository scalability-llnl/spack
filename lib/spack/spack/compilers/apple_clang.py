# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

import llnl.util.lang

import spack.compiler
import spack.compilers.clang
from spack.version import Version


class AppleClang(spack.compilers.clang.Clang):
    openmp_flag = "-Xpreprocessor -fopenmp"

    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        ver = "unknown"
        match = re.search(
            # Apple's LLVM compiler has its own versions, so suffix them.
            r"^Apple (?:LLVM|clang) version ([^ )]+)",
            output,
            # Multi-line, since 'Apple clang' may not be on the first line
            # in particular, when run as gcc, it seems to output
            # "Configured with: --prefix=..." as the first line
            re.M,
        )
        if match:
            ver = match.group(match.lastindex)
        return ver

    # C++ flags based on CMake Modules/Compiler/AppleClang-CXX.cmake

    @property
    def cxx11_flag(self):
        # Spack's AppleClang detection only valid from Xcode >= 4.6
        if self.real_version < Version("4.0"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++11 standard", "cxx11_flag", "Xcode < 4.0"
            )
        return "-std=c++11"

    @property
    def cxx14_flag(self):
        if self.real_version < Version("5.1"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++14 standard", "cxx14_flag", "Xcode < 5.1"
            )
        elif self.real_version < Version("6.1"):
            return "-std=c++1y"

        return "-std=c++14"

    @property
    def cxx17_flag(self):
        if self.real_version < Version("6.1"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++17 standard", "cxx17_flag", "Xcode < 6.1"
            )
        elif self.real_version < Version("10.0"):
            return "-std=c++1z"
        return "-std=c++17"

    @property
    def cxx20_flag(self):
        if self.real_version < Version("10.0"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++20 standard", "cxx20_flag", "Xcode < 10.0"
            )
        elif self.real_version < Version("13.0"):
            return "-std=c++2a"
        return "-std=c++20"

    @property
    def cxx23_flag(self):
        if self.real_version < Version("13.0"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++23 standard", "cxx23_flag", "Xcode < 13.0"
            )
        return "-std=c++2b"

    # C flags based on CMake Modules/Compiler/AppleClang-C.cmake

    @property
    def c99_flag(self):
        if self.real_version < Version("4.0"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C99 standard", "c99_flag", "< 4.0"
            )
        return "-std=c99"

    @property
    def c11_flag(self):
        if self.real_version < Version("4.0"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C11 standard", "c11_flag", "< 4.0"
            )
        return "-std=c11"

    @property
    def c17_flag(self):
        if self.real_version < Version("11.0"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C17 standard", "c17_flag", "< 11.0"
            )
        return "-std=c17"

    @property
    def c23_flag(self):
        if self.real_version < Version("11.0.3"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C23 standard", "c23_flag", "< 11.0.3"
            )
        return "-std=c2x"
