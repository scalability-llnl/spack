# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import llnl.util.tty as tty

from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import Version


class Intel(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ["icc"]

    # Subclasses use possible names of C++ compiler
    cxx_names = ["icpc"]

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ["ifort"]

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ["ifort"]

    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("intel", "icc"),
        "cxx": os.path.join("intel", "icpc"),
        "f77": os.path.join("intel", "ifort"),
        "fc": os.path.join("intel", "ifort"),
    }

    PrgEnv = "PrgEnv-intel"
    PrgEnv_compiler = "intel"

    if sys.platform == "win32":
        version_argument = "/QV"
    else:
        version_argument = "--version"

    if sys.platform == "win32":
        version_regex = r"([1-9][0-9]*\.[0-9]*\.[0-9]*)"
    else:
        version_regex = r"\((?:IFORT|ICC)\) ([^ ]+)"

    @property
    def verbose_flag(self):
        return "-v"

    required_libs = ["libirc", "libifcore", "libifcoremt", "libirng"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Intel deprecated icc/icpc/ifort in 2022. The compilers emit
        # a deprecation warning, but it will be in a log file and
        # difficult to notice. This code adds a spack warning to make
        # it more visible. Making it an error in January 2025 would
        # give people one year to change to %oneapi.
        #
        # The warning is triggered by having an intel toolchain in
        # your compilers.yaml, even if you do not use it.

        # To make it work like package deprecation (error unless
        # --deprecated is passed), then check the value of
        # spack.config.get("config:deprecated", False)
        #
        # spack install
        #
        # accepts the --deprecated argument and sets the spack
        # config. You will need to add support for the --deprecated
        # option to some commands:
        #
        # spack compiler find
        # spack spec
        #
        # I think the error behavior should only happen if you use the
        # compiler, not just includes it in your compilers.yaml. That
        # requires passing info to the wrapper.
        message = (
            "The %intel toolchain has been deprecated."
            "Remove %intel from your compilers.yaml and use %oneapi instead."
        )
        tty.warn(message)

    @property
    def debug_flags(self):
        return ["-debug", "-g", "-g0", "-g1", "-g2", "-g3"]

    @property
    def opt_flags(self):
        return ["-O", "-O0", "-O1", "-O2", "-O3", "-Ofast", "-Os"]

    @property
    def openmp_flag(self):
        if self.real_version < Version("16.0"):
            return "-openmp"
        else:
            return "-qopenmp"

    @property
    def cxx11_flag(self):
        if self.real_version < Version("11.1"):
            raise UnsupportedCompilerFlag(self, "the C++11 standard", "cxx11_flag", "< 11.1")

        elif self.real_version < Version("13"):
            return "-std=c++0x"
        else:
            return "-std=c++11"

    @property
    def cxx14_flag(self):
        # Adapted from CMake's Intel-CXX rules.
        if self.real_version < Version("15"):
            raise UnsupportedCompilerFlag(self, "the C++14 standard", "cxx14_flag", "< 15")
        elif self.real_version < Version("15.0.2"):
            return "-std=c++1y"
        else:
            return "-std=c++14"

    @property
    def cxx17_flag(self):
        # https://www.intel.com/content/www/us/en/developer/articles/news/c17-features-supported-by-c-compiler.html
        if self.real_version < Version("19"):
            raise UnsupportedCompilerFlag(self, "the C++17 standard", "cxx17_flag", "< 19")
        else:
            return "-std=c++17"

    @property
    def c99_flag(self):
        if self.real_version < Version("12"):
            raise UnsupportedCompilerFlag(self, "the C99 standard", "c99_flag", "< 12")
        else:
            return "-std=c99"

    @property
    def c11_flag(self):
        if self.real_version < Version("16"):
            raise UnsupportedCompilerFlag(self, "the C11 standard", "c11_flag", "< 16")
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
        return ("-cxxlib",)
