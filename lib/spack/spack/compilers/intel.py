# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import ver


class Intel(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['icc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['icpc']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['ifort']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['ifort']

    # Named wrapper links within build_env_path
    link_paths = {'cc': 'intel/icc',
                  'cxx': 'intel/icpc',
                  'f77': 'intel/ifort',
                  'fc': 'intel/ifort'}

    PrgEnv = 'PrgEnv-intel'
    PrgEnv_compiler = 'intel'

    version_argument = '--version'
    version_regex = r'\((?:IFORT|ICC)\) ([^ ]+)'

    # Flag defaults for build types
    debug_optimize_flag = ["-02", "-g"]
    debug_max_flag = ["-debug=full"]
    debug_flag = ["-g"]

    @property
    def verbose_flag(self):
        return "-v"

    required_libs = ['libirc', 'libifcore', 'libifcoremt', 'libirng']

    @property
    def debug_flags(self):
        return ['-debug', '-g', '-g0', '-g1', '-g2', '-g3']

    @property
    def opt_flags(self):
        return ['-O', '-O0', '-O1', '-O2', '-O3', '-Ofast', '-Os']

    @property
    def openmp_flag(self):
        if self.real_version < ver('16.0'):
            return "-openmp"
        else:
            return "-qopenmp"

    @property
    def cxx11_flag(self):
        if self.real_version < ver('11.1'):
            raise UnsupportedCompilerFlag(self,
                                          "the C++11 standard",
                                          "cxx11_flag",
                                          "< 11.1")

        elif self.real_version < ver('13'):
            return "-std=c++0x"
        else:
            return "-std=c++11"

    @property
    def cxx14_flag(self):
        # Adapted from CMake's Intel-CXX rules.
        if self.real_version < ver('15'):
            raise UnsupportedCompilerFlag(self,
                                          "the C++14 standard",
                                          "cxx14_flag",
                                          "< 15")
        elif self.real_version < ver('15.0.2'):
            return "-std=c++1y"
        else:
            return "-std=c++14"

    @property
    def c99_flag(self):
        if self.real_version < ver('12'):
            raise UnsupportedCompilerFlag(self,
                                          "the C99 standard",
                                          "c99_flag",
                                          "< 12")
        else:
            return "-std=c99"

    @property
    def c11_flag(self):
        if self.real_version < ver('16'):
            raise UnsupportedCompilerFlag(self,
                                          "the C11 standard",
                                          "c11_flag",
                                          "< 16")
        else:
            return "-std=c1x"

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
        return ('-cxxlib', )
