# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.compiler import Compiler


class Nvhpc(Compiler):
    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("nvhpc", "nvc"),
        "cxx": os.path.join("nvhpc", "nvc++"),
        "f77": os.path.join("nvhpc", "nvfortran"),
        "fc": os.path.join("nvhpc", "nvfortran"),
    }

    version_argument = "--version"
    version_regex = r"nv[^ ]* (?:[^ ]+ Dev-r)?([0-9.]+)(?:-[0-9]+)?"

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def debug_flags(self):
        return ["-g", "-gopt"]

    @property
    def opt_flags(self):
        return ["-O", "-O0", "-O1", "-O2", "-O3", "-O4"]

    @property
    def openmp_flag(self):
        return "-mp"

    @property
    def cc_pic_flag(self):
        return "-fpic"

    @property
    def cxx_pic_flag(self):
        return "-fpic"

    @property
    def f77_pic_flag(self):
        return "-fpic"

    @property
    def fc_pic_flag(self):
        return "-fpic"

    @property
    def c99_flag(self):
        return "-c99"

    @property
    def c11_flag(self):
        return "-c11"

    @property
    def cxx11_flag(self):
        return "--c++11"

    @property
    def cxx14_flag(self):
        return "--c++14"

    @property
    def cxx17_flag(self):
        return "--c++17"

    @property
    def stdcxx_libs(self):
        return ("-c++libs",)

    required_libs = ["libnvc", "libnvf"]
