# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import Version


class Pgi(Compiler):
    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("pgi", "pgcc"),
        "cxx": os.path.join("pgi", "pgc++"),
        "f77": os.path.join("pgi", "pgfortran"),
        "fc": os.path.join("pgi", "pgfortran"),
    }

    version_argument = "-V"
    ignore_version_errors = [2]  # `pgcc -V` on PowerPC annoyingly returns 2
    version_regex = r"pg[^ ]* ([0-9.]+)-[0-9]+ (LLVM )?[^ ]+ target on "

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
    def cxx11_flag(self):
        return "-std=c++11"

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

    required_libs = ["libpgc", "libpgf90"]

    @property
    def c99_flag(self):
        if self.real_version >= Version("12.10"):
            return "-c99"
        raise UnsupportedCompilerFlag(self, "the C99 standard", "c99_flag", "< 12.10")

    @property
    def c11_flag(self):
        if self.real_version >= Version("15.3"):
            return "-c11"
        raise UnsupportedCompilerFlag(self, "the C11 standard", "c11_flag", "< 15.3")

    @property
    def stdcxx_libs(self):
        return ("-pgc++libs",)
