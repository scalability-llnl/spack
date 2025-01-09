# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.compiler


class Fj(spack.compiler.Compiler):
    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("fj", "fcc"),
        "cxx": os.path.join("fj", "case-insensitive", "FCC"),
        "f77": os.path.join("fj", "frt"),
        "fc": os.path.join("fj", "frt"),
    }

    version_argument = "--version"
    version_regex = r"\((?:FCC|FRT)\) ([a-z\d.]+)"

    required_libs = ["libfj90i", "libfj90f", "libfjsrcinfo"]

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def debug_flags(self):
        return "-g"

    @property
    def opt_flags(self):
        return ["-O0", "-O1", "-O2", "-O3", "-Ofast"]

    @property
    def openmp_flag(self):
        return "-Kopenmp"

    @property
    def cxx98_flag(self):
        return "-std=c++98"

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
        return "-KPIC"

    @property
    def cxx_pic_flag(self):
        return "-KPIC"

    @property
    def f77_pic_flag(self):
        return "-KPIC"

    @property
    def fc_pic_flag(self):
        return "-KPIC"
