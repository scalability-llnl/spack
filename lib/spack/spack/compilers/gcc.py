# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from llnl.util.filesystem import ancestor

import spack.compiler
import spack.compilers.apple_clang as apple_clang
import spack.util.executable
from spack.version import Version


class Gcc(spack.compiler.Compiler):
    # MacPorts builds gcc versions with prefixes and -mp-X or -mp-X.Y suffixes.
    # Homebrew and Linuxbrew may build gcc with -X, -X.Y suffixes.
    # Old compatibility versions may contain XY suffixes.
    suffixes = [r"-mp-\d+(?:\.\d+)?", r"-\d+(?:\.\d+)?", r"\d\d"]

    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("gcc", "gcc"),
        "cxx": os.path.join("gcc", "g++"),
        "f77": os.path.join("gcc", "gfortran"),
        "fc": os.path.join("gcc", "gfortran"),
    }

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def debug_flags(self):
        return ["-g", "-gstabs+", "-gstabs", "-gxcoff+", "-gxcoff", "-gvms"]

    @property
    def opt_flags(self):
        return ["-O", "-O0", "-O1", "-O2", "-O3", "-Os", "-Ofast", "-Og"]

    @property
    def openmp_flag(self):
        return "-fopenmp"

    @property
    def cxx98_flag(self):
        if self.real_version < Version("6.0"):
            return ""
        else:
            return "-std=c++98"

    @property
    def cxx11_flag(self):
        if self.real_version < Version("4.3"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++11 standard", "cxx11_flag", " < 4.3"
            )
        elif self.real_version < Version("4.7"):
            return "-std=c++0x"
        else:
            return "-std=c++11"

    @property
    def cxx14_flag(self):
        if self.real_version < Version("4.8"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++14 standard", "cxx14_flag", "< 4.8"
            )
        elif self.real_version < Version("4.9"):
            return "-std=c++1y"
        else:
            return "-std=c++14"

    @property
    def cxx17_flag(self):
        if self.real_version < Version("5.0"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++17 standard", "cxx17_flag", "< 5.0"
            )
        elif self.real_version < Version("6.0"):
            return "-std=c++1z"
        else:
            return "-std=c++17"

    @property
    def cxx20_flag(self):
        if self.real_version < Version("8.0"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++20 standard", "cxx20_flag", "< 8.0"
            )
        elif self.real_version < Version("11.0"):
            return "-std=c++2a"
        else:
            return "-std=c++20"

    @property
    def cxx23_flag(self):
        if self.real_version < Version("11.0"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C++23 standard", "cxx23_flag", "< 11.0"
            )
        elif self.real_version < Version("14.0"):
            return "-std=c++2b"
        else:
            return "-std=c++23"

    @property
    def c99_flag(self):
        if self.real_version < Version("4.5"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C99 standard", "c99_flag", "< 4.5"
            )
        return "-std=c99"

    @property
    def c11_flag(self):
        if self.real_version < Version("4.7"):
            raise spack.compiler.UnsupportedCompilerFlag(
                self, "the C11 standard", "c11_flag", "< 4.7"
            )
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

    required_libs = ["libgcc", "libgfortran"]

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
        if apple_clang.AppleClang.default_version(cc) != "unknown":
            return "unknown"

        version = super(Gcc, cls).default_version(cc)
        if Version(version) >= Version("7"):
            output = spack.compiler.get_compiler_version_output(cc, "-dumpfullversion")
            version = cls.extract_version_from_output(output)
        return version

    @property
    def stdcxx_libs(self):
        return ("-lstdc++",)

    @property
    def prefix(self):
        # GCC reports its install prefix when running ``-print-search-dirs``
        # on the first line ``install: <prefix>``.
        cc = spack.util.executable.Executable(self.cc)
        with self.compiler_environment():
            gcc_output = cc("-print-search-dirs", output=str, error=str)

            for line in gcc_output.splitlines():
                if line.startswith("install:"):
                    gcc_prefix = line.split(":")[1].strip()
                    # Go from <prefix>/lib/gcc/<triplet>/<version>/ to <prefix>
                    return ancestor(gcc_prefix, 4)

            raise RuntimeError(
                "could not find install prefix of GCC from output:\n\t{}".format(gcc_output)
            )
