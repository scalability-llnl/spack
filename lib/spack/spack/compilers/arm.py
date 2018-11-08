# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.compiler import Compiler, _version_cache
from spack.util.executable import Executable


class Arm(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['armclang']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['armclang++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['armflang']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['armflang']

    # Named wrapper links within lib/spack/env
    link_paths = {'cc': 'clang/clang',
                  'cxx': 'clang/clang++',
                  'f77': 'clang/flang',
                  'fc': 'clang/flang'}

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
        return "-std=c++1z"

    @property
    def pic_flag(self):
        return "-fPIC"

    @classmethod
    def default_version(cls, comp):
        """The ``--version`` option seems to be the most consistent one
        for arm compilers.  Output looks like this::

            $ arm<c/f>lang --version
            Arm C/C++/Fortran Compiler version 19.0 (build number 73) (based on LLVM 7.0.2)
            Target: aarch64--linux-gnu
            Thread model: posix
            InstalledDir: /opt/arm/arm-hpc-compiler-19.0_Generic-AArch64_RHEL-7_aarch64-linux/bin
        """
        return get_compiler_version(
            comp, '--version', r'\((?:Arm)\) ([^ ]+)')

    @classmethod
    def fc_version(cls, fc):
        return cls.default_version(fc)

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)
