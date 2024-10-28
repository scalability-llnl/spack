# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import llnl.util.lang

from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import Version

#: compiler symlink mappings for mixed f77 compilers
f77_mapping = [
    ("gfortran", os.path.join("clang", "gfortran")),
    ("xlf_r", os.path.join("xl_r", "xlf_r")),
    ("xlf", os.path.join("xl", "xlf")),
    ("pgfortran", os.path.join("pgi", "pgfortran")),
    ("ifort", os.path.join("intel", "ifort")),
]

#: compiler symlink mappings for mixed f90/fc compilers
fc_mapping = [
    ("gfortran", os.path.join("clang", "gfortran")),
    ("xlf90_r", os.path.join("xl_r", "xlf90_r")),
    ("xlf90", os.path.join("xl", "xlf90")),
    ("pgfortran", os.path.join("pgi", "pgfortran")),
    ("ifort", os.path.join("intel", "ifort")),
]


class Clang(Compiler):
    version_argument = "--version"

    @property
    def debug_flags(self):
        return [
            "-gcodeview",
            "-gdwarf-2",
            "-gdwarf-3",
            "-gdwarf-4",
            "-gdwarf-5",
            "-gline-tables-only",
            "-gmodules",
            "-g",
        ]

    @property
    def opt_flags(self):
        return ["-O0", "-O1", "-O2", "-O3", "-Ofast", "-Os", "-Oz", "-Og", "-O", "-O4"]

    # Clang has support for using different fortran compilers with the
    # clang executable.
    @property
    def link_paths(self):
        # clang links are always the same
        link_paths = {
            "cc": os.path.join("clang", "clang"),
            "cxx": os.path.join("clang", "clang++"),
        }

        # fortran links need to look at the actual compiler names from
        # compilers.yaml to figure out which named symlink to use
        for compiler_name, link_path in f77_mapping:
            if self.f77 and compiler_name in self.f77:
                link_paths["f77"] = link_path
                break
        else:
            link_paths["f77"] = os.path.join("clang", "flang")

        for compiler_name, link_path in fc_mapping:
            if self.fc and compiler_name in self.fc:
                link_paths["fc"] = link_path
                break
        else:
            link_paths["fc"] = os.path.join("clang", "flang")

        return link_paths

    @property
    def verbose_flag(self):
        return "-v"

    openmp_flag = "-fopenmp"

    # C++ flags based on CMake Modules/Compiler/Clang.cmake

    @property
    def cxx11_flag(self):
        if self.real_version < Version("3.3"):
            raise UnsupportedCompilerFlag(self, "the C++11 standard", "cxx11_flag", "< 3.3")
        return "-std=c++11"

    @property
    def cxx14_flag(self):
        if self.real_version < Version("3.4"):
            raise UnsupportedCompilerFlag(self, "the C++14 standard", "cxx14_flag", "< 3.5")
        elif self.real_version < Version("3.5"):
            return "-std=c++1y"

        return "-std=c++14"

    @property
    def cxx17_flag(self):
        if self.real_version < Version("3.5"):
            raise UnsupportedCompilerFlag(self, "the C++17 standard", "cxx17_flag", "< 3.5")
        elif self.real_version < Version("5.0"):
            return "-std=c++1z"

        return "-std=c++17"

    @property
    def cxx20_flag(self):
        if self.real_version < Version("5.0"):
            raise UnsupportedCompilerFlag(self, "the C++20 standard", "cxx20_flag", "< 5.0")
        elif self.real_version < Version("11.0"):
            return "-std=c++2a"
        else:
            return "-std=c++20"

    @property
    def cxx23_flag(self):
        if self.real_version < Version("12.0"):
            raise UnsupportedCompilerFlag(self, "the C++23 standard", "cxx23_flag", "< 12.0")
        elif self.real_version < Version("17.0"):
            return "-std=c++2b"
        else:
            return "-std=c++23"

    @property
    def c99_flag(self):
        return "-std=c99"

    @property
    def c11_flag(self):
        if self.real_version < Version("3.0"):
            raise UnsupportedCompilerFlag(self, "the C11 standard", "c11_flag", "< 3.0")
        if self.real_version < Version("3.1"):
            return "-std=c1x"
        return "-std=c11"

    @property
    def c17_flag(self):
        if self.real_version < Version("6.0"):
            raise UnsupportedCompilerFlag(self, "the C17 standard", "c17_flag", "< 6.0")
        return "-std=c17"

    @property
    def c23_flag(self):
        if self.real_version < Version("9.0"):
            raise UnsupportedCompilerFlag(self, "the C23 standard", "c23_flag", "< 9.0")
        elif self.real_version < Version("18.0"):
            return "-std=c2x"
        else:
            return "-std=c23"

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

    required_libs = ["libclang"]

    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        ver = "unknown"
        if ("Apple" in output) or ("AMD" in output):
            return ver

        match = re.search(
            # Normal clang compiler versions are left as-is
            r"(?:clang|flang-new) version ([^ )\n]+)-svn[~.\w\d-]*|"
            # Don't include hyphenated patch numbers in the version
            # (see https://github.com/spack/spack/pull/14365 for details)
            r"(?:clang|flang-new) version ([^ )\n]+?)-[~.\w\d-]*|"
            r"(?:clang|flang-new) version ([^ )\n]+)",
            output,
        )
        if match:
            ver = match.group(match.lastindex)
        return ver
