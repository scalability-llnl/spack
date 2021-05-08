# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import Compiler


class Nvhpc(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['nvc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['nvc++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['nvfortran']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['nvfortran']

    # Named wrapper links within build_env_path
    link_paths = {'cc':  'nvhpc/nvc',
                  'cxx': 'nvhpc/nvc++',
                  'f77': 'nvhpc/nvfortran',
                  'fc':  'nvhpc/nvfortran'}

    PrgEnv = 'PrgEnv-nvhpc'
    PrgEnv_compiler = 'nvhpc'

    version_argument = '--version'
    version_regex = r'nv[^ ]* (?:[^ ]+ Dev-r)?([0-9.]+)(?:-[0-9]+)?'

    # https://docs.nvidia.com/hpc-sdk/compilers/hpc-compilers-user-guide/
    debug_optimize_flag = ["-⁠gopt"]
    debug_max_flag = ["-g"]
    debug_flag = ["-g"]

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def debug_flags(self):
        return ['-g', '-gopt']

    @property
    def opt_flags(self):
        return ['-O', '-O0', '-O1', '-O2', '-O3', '-O4']

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
        return '-c99'

    @property
    def c11_flag(self):
        return '-c11'

    @property
    def cxx11_flag(self):
        return '--c++11'

    @property
    def cxx14_flag(self):
        return '--c++14'

    @property
    def cxx17_flag(self):
        return '--c++17'

    @property
    def stdcxx_libs(self):
        return ('-c++libs', )

    required_libs = ['libnvc', 'libnvf']
