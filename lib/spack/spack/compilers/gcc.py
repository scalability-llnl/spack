# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import spack.compiler
import spack.compilers.apple_clang as apple_clang

from spack.version import ver


class Gcc(spack.compiler.Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['gcc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['g++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['gfortran']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['gfortran']

    # MacPorts builds gcc versions with prefixes and -mp-X.Y suffixes.
    # Homebrew and Linuxbrew may build gcc with -X, -X.Y suffixes.
    # Old compatibility versions may contain XY suffixes.
    suffixes = [r'-mp-\d+\.\d+', r'-\d+\.\d+', r'-\d+', r'\d\d']

    # Named wrapper links within build_env_path
    link_paths = {'cc': 'gcc/gcc',
                  'cxx': 'gcc/g++',
                  'f77': 'gcc/gfortran',
                  'fc': 'gcc/gfortran'}

    PrgEnv = 'PrgEnv-gnu'
    PrgEnv_compiler = 'gcc'

    # Flag defaults for build types
    debug_optimize_flag = ["-g3", "-grecord-gcc-switches",
                           "-fvar-tracking-assignments",
                           "-gstatement-frontiers",
                           "-gvariable-location-views",
                           "-O2"]

    debug_max_flag = ["-g3", "-fvar-tracking-assignments",
                      "-gstatement-frontiers",
                      "-gvariable-location-views",
                      "-grecord-gcc-switches",
                      "-Wall", "-Werror=format-security",
                      "-Wp,-D_FORTIFY_SOURCE=2",
                      "-fexceptions",
                      "-Wp,-D_GLIBCXX_ASSERTIONS",
                      "-fstack-protector-strong",
                      "-fstack-clash-protection",
                      "-fcf-protection",
                      "-fasynchronous-unwind-tables",
                      "-fallow-argument-mismatch"]

    debug_flag = ["-g3", "-grecord-gcc-switches", "-Og"]

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def debug_flags(self):
        return ['-g', '-gstabs+', '-gstabs', '-gxcoff+', '-gxcoff', '-gvms']

    @property
    def opt_flags(self):
        return ['-O', '-O0', '-O1', '-O2', '-O3', '-Os', '-Ofast', '-Og']

    @property
    def openmp_flag(self):
        return "-fopenmp"

    @property
    def cxx98_flag(self):
        if self.real_version < ver('6.0'):
            return ""
        else:
            return "-std=c++98"

    @property
    def cxx11_flag(self):
        if self.real_version < ver('4.3'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++11 standard", "cxx11_flag", " < 4.3")
        elif self.real_version < ver('4.7'):
            return "-std=c++0x"
        else:
            return "-std=c++11"

    @property
    def cxx14_flag(self):
        if self.real_version < ver('4.8'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++14 standard", "cxx14_flag", "< 4.8")
        elif self.real_version < ver('4.9'):
            return "-std=c++1y"
        elif self.real_version < ver('6.0'):
            return "-std=c++14"
        else:
            return ""

    @property
    def cxx17_flag(self):
        if self.real_version < ver('5.0'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++17 standard", "cxx17_flag", "< 5.0")
        elif self.real_version < ver('6.0'):
            return "-std=c++1z"
        else:
            return "-std=c++17"

    @property
    def c99_flag(self):
        if self.real_version < ver('4.5'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C99 standard", "c99_flag", "< 4.5")
        return "-std=c99"

    @property
    def c11_flag(self):
        if self.real_version < ver('4.7'):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C11 standard", "c11_flag", "< 4.7")
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

    required_libs = ['libgcc', 'libgfortran']

    @classmethod
    def default_version(cls, cc):
        """Older versions of gcc use the ``-dumpversion`` option.
        Output looks like this::

            4.4.7

        In GCC 7, this option was changed to only return the major
        version of the compiler::

            7

        A new ``-dumpfullversion`` option was added that gives us
        what we want::

            7.2.0
        """
        # Apple's gcc is actually apple clang, so skip it. Returning
        # "unknown" ensures this compiler is not detected by default.
        # Users can add it manually to compilers.yaml at their own risk.
        if apple_clang.AppleClang.default_version(cc) != 'unknown':
            return 'unknown'

        version = super(Gcc, cls).default_version(cc)
        if ver(version) >= ver('7'):
            output = spack.compiler.get_compiler_version_output(
                cc, '-dumpfullversion'
            )
            version = cls.extract_version_from_output(output)
        return version

    @classmethod
    def fc_version(cls, fc):
        """Older versions of gfortran use the ``-dumpversion`` option.
        Output looks like this::

            GNU Fortran (GCC) 4.4.7 20120313 (Red Hat 4.4.7-18)
            Copyright (C) 2010 Free Software Foundation, Inc.

        or::

            4.8.5

        In GCC 7, this option was changed to only return the major
        version of the compiler::

            7

        A new ``-dumpfullversion`` option was added that gives us
        what we want::

            7.2.0
        """
        output = spack.compiler.get_compiler_version_output(fc, '-dumpversion')
        match = re.search(r'(?:GNU Fortran \(GCC\) )?([\d.]+)', output)
        version = match.group(match.lastindex) if match else 'unknown'
        if ver(version) >= ver('7'):
            output = spack.compiler.get_compiler_version_output(
                fc, '-dumpfullversion'
            )
            version = cls.extract_version_from_output(output)
        return version

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)

    @property
    def stdcxx_libs(self):
        return ('-lstdc++', )
