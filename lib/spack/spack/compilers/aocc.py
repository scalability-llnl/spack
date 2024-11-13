# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import llnl.util.lang

from spack.compiler import Compiler
from spack.version import ver


class Aocc(Compiler):
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

    @property
    def link_paths(self):
        link_paths = {
            "cc": os.path.join("aocc", "clang"),
            "cxx": os.path.join("aocc", "clang++"),
            "f77": os.path.join("aocc", "flang"),
            "fc": os.path.join("aocc", "flang"),
        }

        return link_paths

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def openmp_flag(self):
        return "-fopenmp"

    @property
    def cxx11_flag(self):
        return "-std=c++11"

    @property
    def cxx14_flag(self):
        return "-std=c++14"

    @property
    def cxx17_flag(self):
        return "-std=c++17"

    @property
    def c99_flag(self):
        return "-std=c99"

    @property
    def c11_flag(self):
        return "-std=c11"

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
        match = re.search(r"AOCC_(\d+)[._](\d+)[._](\d+)", output)
        if match:
            return ".".join(match.groups())
        return "unknown"

    @property
    def stdcxx_libs(self):
        return ("-lstdc++",)

    @property
    def cflags(self):
        return self._handle_default_flag_addtions()

    @property
    def cxxflags(self):
        return self._handle_default_flag_addtions()

    @property
    def fflags(self):
        return self._handle_default_flag_addtions()

    def _handle_default_flag_addtions(self):
        # This is a known issue for AOCC 3.0 see:
        # https://developer.amd.com/wp-content/resources/AOCC-3.0-Install-Guide.pdf
        if self.real_version.satisfies(ver("3.0.0")):
            return "-Wno-unused-command-line-argument " "-mllvm -eliminate-similar-expr=false"
