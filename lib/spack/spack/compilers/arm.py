# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.compiler
import re


class Arm(spack.compiler.Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['armclang']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['armclang++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['armflang']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['armflang']

    # Named wrapper links within lib/spack/env
    link_paths = {'cc': 'arm/armclang',
                  'cxx': 'arm/armclang++',
                  'f77': 'arm/armflang',
                  'fc': 'arm/armflang'}

    debug_optimize_flag = ["-g", "-O2"]
    debug_max_flag = ["-g"]
    debug_flag = ["-g"]

    # The ``--version`` option seems to be the most consistent one for
    # arm compilers. Output looks like this:
    #
    # $ arm<c/f>lang --version
    # Arm C/C++/Fortran Compiler version 19.0 (build number 73) (based on LLVM 7.0.2) # NOQA
    # Target: aarch64--linux-gnu
    # Thread model: posix
    # InstalledDir:
    # /opt/arm/arm-hpc-compiler-19.0_Generic-AArch64_RHEL-7_aarch64-linux/bin
    version_argument = '--version'
    version_regex = r'Arm C\/C\+\+\/Fortran Compiler version ([\d\.]+) '\
                    r'\(build number (\d+)\) '

    @classmethod
    def extract_version_from_output(cls, output):
        """Extracts the version from compiler's output."""
        match = re.search(cls.version_regex, output)
        temp = 'unknown'
        if match:
            if match.group(1).count('.') == 1:
                temp = match.group(1) + ".0." + match.group(2)
            else:
                temp = match.group(1) + "." + match.group(2)
        return temp

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def opt_flags(self):
        return ['-O', '-O0', '-O1', '-O2', '-O3', '-Ofast']

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
    def c99_flag(self):
        return "-std=c99"

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

    required_libs = ['libclang', 'libflang']

    @classmethod
    def fc_version(cls, fc):
        return cls.default_version(fc)

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)
