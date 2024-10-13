# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import Version


class Intel(Compiler):
    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("intel", "icc"),
        "cxx": os.path.join("intel", "icpc"),
        "f77": os.path.join("intel", "ifort"),
        "fc": os.path.join("intel", "ifort"),
    }

    if sys.platform == "win32":
        version_argument = "/QV"
    else:
        version_argument = "--version"

    if sys.platform == "win32":
        version_regex = r"([1-9][0-9]*\.[0-9]*\.[0-9]*)"
    else:
        version_regex = r"\((?:IFORT|ICC)\) ([^ ]+)"

    @property
    def verbose_flag(self):
        return "-v"

    required_libs = ["libirc", "libifcore", "libifcoremt", "libirng"]

    @property
    def debug_flags(self):
        return ["-debug", "-g", "-g0", "-g1", "-g2", "-g3"]

    @property
    def opt_flags(self):
        return ["-O", "-O0", "-O1", "-O2", "-O3", "-Ofast", "-Os"]

    @property
    def openmp_flag(self):
        if self.real_version < Version("16.0"):
            return "-openmp"
        else:
            return "-qopenmp"

    @property
    def cxx11_flag(self):
        if self.real_version < Version("11.1"):
            raise UnsupportedCompilerFlag(self, "the C++11 standard", "cxx11_flag", "< 11.1")

        elif self.real_version < Version("13"):
            return "-std=c++0x"
        else:
            return "-std=c++11"

    @property
    def cxx14_flag(self):
        # Adapted from CMake's Intel-CXX rules.
        if self.real_version < Version("15"):
            raise UnsupportedCompilerFlag(self, "the C++14 standard", "cxx14_flag", "< 15")
        elif self.real_version < Version("15.0.2"):
            return "-std=c++1y"
        else:
            return "-std=c++14"

    @property
    def cxx17_flag(self):
        # https://www.intel.com/content/www/us/en/developer/articles/news/c17-features-supported-by-c-compiler.html
        if self.real_version < Version("19"):
            raise UnsupportedCompilerFlag(self, "the C++17 standard", "cxx17_flag", "< 19")
        else:
            return "-std=c++17"

    @property
    def c99_flag(self):
        if self.real_version < Version("12"):
            raise UnsupportedCompilerFlag(self, "the C99 standard", "c99_flag", "< 12")
        else:
            return "-std=c99"

    @property
    def c11_flag(self):
        if self.real_version < Version("16"):
            raise UnsupportedCompilerFlag(self, "the C11 standard", "c11_flag", "< 16")
        else:
            return "-std=c1x"

    @property
    def c18_flag(self):
        # c18 supported since oneapi 2022, which is classic version 2021.5.0
        if self.real_version < Version("21.5.0"):
            raise UnsupportedCompilerFlag(self, "the C18 standard", "c18_flag", "< 21.5.0")
        else:
            return "-std=c18"

    @property
    def cc_pic_flag(self):
        return "-fPIC"

    @property
    def cxx_pic_flag(self):
        return "-fPIC"

    @property
    def f77_pic_flag(self):
        return "-fPIC"

    @property
    def fc_pic_flag(self):
        return "-fPIC"

    @property
    def stdcxx_libs(self):
        return ("-cxxlib",)

    def setup_custom_environment(self, pkg, env):
        # Edge cases for Intel's oneAPI compilers when using the legacy classic compilers:
        # Always pass flags to disable deprecation warnings, since these warnings can
        # confuse tools that parse the output of compiler commands (e.g. version checks).
        if self.cc and self.cc.endswith("icc") and self.real_version >= Version("2021"):
            env.append_flags("SPACK_ALWAYS_CFLAGS", "-diag-disable=10441")
        if self.cxx and self.cxx.endswith("icpc") and self.real_version >= Version("2021"):
            env.append_flags("SPACK_ALWAYS_CXXFLAGS", "-diag-disable=10441")
        if self.fc and self.fc.endswith("ifort") and self.real_version >= Version("2021"):
            env.append_flags("SPACK_ALWAYS_FFLAGS", "-diag-disable=10448")
