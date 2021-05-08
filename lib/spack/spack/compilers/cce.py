# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import ver


class Cce(Compiler):
    """Cray compiler environment compiler."""
    # Subclasses use possible names of C compiler
    cc_names = ['cc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['CC']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['ftn']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['ftn']

    # MacPorts builds gcc versions with prefixes and -mp-X.Y suffixes.
    suffixes = [r'-mp-\d\.\d']

    PrgEnv = 'PrgEnv-cray'
    PrgEnv_compiler = 'cce'

    link_paths = {'cc': 'cce/cc',
                  'cxx': 'cce/case-insensitive/CC',
                  'f77': 'cce/ftn',
                  'fc': 'cce/ftn'}

    # https://user.cscs.ch/computing/compilation/cray/
    debug_optimize_flag = ["-G02"]
    debug_max_flag = ["-g"]
    debug_flag = ["-g"]

    @property
    def is_clang_based(self):
        version = self._real_version or self.version
        return version >= ver('9.0') and 'classic' not in str(version)

    @property
    def version_argument(self):
        if self.is_clang_based:
            return '--version'
        return '-V'

    version_regex = r'[Vv]ersion.*?(\d+(\.\d+)+)'

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def debug_flags(self):
        return ['-g', '-G0', '-G1', '-G2', '-Gfast']

    @property
    def openmp_flag(self):
        if self.is_clang_based:
            return '-fopenmp'
        return "-h omp"

    @property
    def cxx11_flag(self):
        if self.is_clang_based:
            return '-std=c++11'
        return "-h std=c++11"

    @property
    def c99_flag(self):
        if self.is_clang_based:
            return '-std=c99'
        elif self.real_version >= ver('8.4'):
            return '-h std=c99,noconform,gnu'
        elif self.real_version >= ver('8.1'):
            return '-h c99,noconform,gnu'
        raise UnsupportedCompilerFlag(self,
                                      'the C99 standard',
                                      'c99_flag',
                                      '< 8.1')

    @property
    def c11_flag(self):
        if self.is_clang_based:
            return '-std=c11'
        elif self.real_version >= ver('8.5'):
            return '-h std=c11,noconform,gnu'
        raise UnsupportedCompilerFlag(self,
                                      'the C11 standard',
                                      'c11_flag',
                                      '< 8.5')

    @property
    def cc_pic_flag(self):
        if self.is_clang_based:
            return "-fPIC"
        return "-h PIC"

    @property
    def cxx_pic_flag(self):
        if self.is_clang_based:
            return "-fPIC"
        return "-h PIC"

    @property
    def f77_pic_flag(self):
        if self.is_clang_based:
            return "-fPIC"
        return "-h PIC"

    @property
    def fc_pic_flag(self):
        if self.is_clang_based:
            return "-fPIC"
        return "-h PIC"

    @property
    def stdcxx_libs(self):
        # Cray compiler wrappers link to the standard C++ library
        # without additional flags.
        return ()
