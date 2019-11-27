# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import ver


class Pgi(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['pgcc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['pgc++', 'pgCC']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['pgfortran', 'pgf77']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['pgfortran', 'pgf95', 'pgf90']

    # Named wrapper links within build_env_path
    link_paths = {'cc': 'pgi/pgcc',
                  'cxx': 'pgi/pgc++',
                  'f77': 'pgi/pgfortran',
                  'fc': 'pgi/pgfortran'}

    cray_prgenv_name = 'PrgEnv-pgi'
    cray_module_name = 'pgi'

    version_argument = '-V'
    version_regex = r'pg[^ ]* ([0-9.]+)-[0-9]+ (LLVM )?[^ ]+ target on '

    @classmethod
    def verbose_flag(cls):
        return "-v"

    @property
    def openmp_flag(self):
        return "-mp"

    @property
    def cxx11_flag(self):
        return "-std=c++11"

    @property
    def pic_flag(self):
        return "-fpic"

    required_libs = ['libpgc', 'libpgf90']

    @property
    def c99_flag(self):
        if self.version >= ver('12.10'):
            return '-c99'
        raise UnsupportedCompilerFlag(self,
                                      'the C99 standard',
                                      'c99_flag',
                                      '< 12.10')

    @property
    def c11_flag(self):
        if self.version >= ver('15.3'):
            return '-c11'
        raise UnsupportedCompilerFlag(self,
                                      'the C11 standard',
                                      'c11_flag',
                                      '< 15.3')
