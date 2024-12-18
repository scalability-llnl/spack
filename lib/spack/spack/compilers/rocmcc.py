# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import llnl.util.lang

import spack.compilers.clang


class Rocmcc(spack.compilers.clang.Clang):
    @property
    def link_paths(self):
        link_paths = {
            "cc": "rocmcc/amdclang",
            "cxx": "rocmcc/amdclang++",
            "f77": "rocmcc/amdflang",
            "fc": "rocmcc/amdflang",
        }

        return link_paths

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

    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        match = re.search(r"llvm-project roc-(\d+)[._](\d+)[._](\d+)", output)
        if match:
            return ".".join(match.groups())

    @property
    def stdcxx_libs(self):
        return ("-lstdc++",)
