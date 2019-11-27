# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    cray_prgenv_name = 'PrgEnv-cray'
    cray_module_name = 'cce'

    link_paths = {'cc': 'cce/cc',
                  'cxx': 'cce/case-insensitive/CC',
                  'f77': 'cce/ftn',
                  'fc': 'cce/ftn'}

    version_argument = '-V'
    version_regex = r'[Vv]ersion.*?(\d+(\.\d+)+)'

    @classmethod
    def verbose_flag(cls):
        return "-v"

    @property
    def openmp_flag(self):
        return "-h omp"

    @property
    def cxx11_flag(self):
        return "-h std=c++11"

    @property
    def c99_flag(self):
        if self.version >= ver('8.4'):
            return '-h stc=c99,noconform,gnu'
        if self.version >= ver('8.1'):
            return '-h c99,noconform,gnu'
        raise UnsupportedCompilerFlag(self,
                                      'the C99 standard',
                                      'c99_flag',
                                      '< 8.1')

    @property
    def c11_flag(self):
        if self.version >= ver('8.5'):
            return '-h std=c11,noconform,gnu'
        raise UnsupportedCompilerFlag(self,
                                      'the C11 standard',
                                      'c11_flag',
                                      '< 8.5')

    @property
    def pic_flag(self):
        return "-h PIC"
