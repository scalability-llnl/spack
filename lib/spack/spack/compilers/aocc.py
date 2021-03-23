# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

import llnl.util.lang

from spack.compiler import Compiler
from spack.version import ver


class Aocc(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['clang']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['clang++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['flang']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['flang']

    version_argument = '--version'

    @property
    def debug_flags(self):
        return ['-gcodeview', '-gdwarf-2', '-gdwarf-3', '-gdwarf-4',
                '-gdwarf-5', '-gline-tables-only', '-gmodules', '-gz', '-g']

    @property
    def opt_flags(self):
        return ['-O0', '-O1', '-O2', '-O3', '-Ofast', '-Os', '-Oz', '-Og',
                '-O', '-O4']

    @property
    def link_paths(self):
        link_paths = {'cc': 'aocc/clang',
                      'cxx': 'aocc/clang++',
                      'f77': 'aocc/flang',
                      'fc': 'aocc/flang'}

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
        return '-std=c99'

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

    required_libs = ['libclang']

    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        loc_ver = 'unknown'

        match = re.search(
            r'AMD clang version ([^ )]+)',
            output
        )
        if match:
            loc_ver = output.split('AOCC_')[1].split('-')[0]
        return loc_ver

    @classmethod
    def fc_version(cls, fortran_compiler):
        if sys.platform == 'darwin':
            return cls.default_version('clang')

        return cls.default_version(fortran_compiler)

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)

    @property
    def stdcxx_libs(self):
        return ('-lstdc++', )

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
        if self.real_version == ver('3.0.0'):
            return ("-Wno-unused-command-line-argument "
                    "-mllvm -eliminate-similar-expr=false")
