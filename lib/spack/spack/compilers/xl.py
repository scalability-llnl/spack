# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import Version


class Xl(Compiler):
    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("xl", "xlc"),
        "cxx": os.path.join("xl", "xlc++"),
        "f77": os.path.join("xl", "xlf"),
        "fc": os.path.join("xl", "xlf90"),
    }

    version_argument = "-qversion"
    version_regex = r"([0-9]?[0-9]\.[0-9])"

    @property
    def verbose_flag(self):
        return "-V"

    @property
    def debug_flags(self):
        return ["-g", "-g0", "-g1", "-g2", "-g8", "-g9"]

    @property
    def opt_flags(self):
        return ["-O", "-O0", "-O1", "-O2", "-O3", "-O4", "-O5", "-Ofast"]

    @property
    def openmp_flag(self):
        return "-qsmp=omp"

    @property
    def cxx11_flag(self):
        if self.real_version < Version("13.1"):
            raise UnsupportedCompilerFlag(self, "the C++11 standard", "cxx11_flag", "< 13.1")
        else:
            return "-qlanglvl=extended0x"

    @property
    def c99_flag(self):
        if self.real_version >= Version("13.1.1"):
            return "-std=gnu99"
        if self.real_version >= Version("10.1"):
            return "-qlanglvl=extc99"
        raise UnsupportedCompilerFlag(self, "the C99 standard", "c99_flag", "< 10.1")

    @property
    def c11_flag(self):
        if self.real_version >= Version("13.1.2"):
            return "-std=gnu11"
        if self.real_version >= Version("12.1"):
            return "-qlanglvl=extc1x"
        raise UnsupportedCompilerFlag(self, "the C11 standard", "c11_flag", "< 12.1")

    @property
    def cxx14_flag(self):
        # .real_version does not have the "y.z" component of "w.x.y.z", which
        # is required to distinguish whether support is available
        if self.version >= Version("16.1.1.8"):
            return "-std=c++14"
        raise UnsupportedCompilerFlag(self, "the C++14 standard", "cxx14_flag", "< 16.1.1.8")

    @property
    def cc_pic_flag(self):
        return "-qpic"

    @property
    def cxx_pic_flag(self):
        return "-qpic"

    @property
    def f77_pic_flag(self):
        return "-qpic"

    @property
    def fc_pic_flag(self):
        return "-qpic"

    @property
    def fflags(self):
        # The -qzerosize flag is effective only for the Fortran 77
        # compilers and allows the use of zero size objects.
        # For Fortran 90 and beyond, it is set by default and has not impact.
        # Its use has no negative side effects.
        return "-qzerosize"
