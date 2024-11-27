# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gcc(CompilerPackage, Package):
    """Simple compiler package."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/gcc-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("3.0", md5="def0123456789abcdef0123456789abc")

    variant(
        "languages",
        default="c,c++,fortran",
        values=("c", "c++", "fortran"),
        multi=True,
        description="Compilers and runtime libraries to build",
    )

    depends_on("conflict", when="@3.0")

    c_names = ["gcc"]
    cxx_names = ["g++"]
    fortran_names = ["gfortran"]
    compiler_prefixes = [r"\w+-\w+-\w+-"]
    compiler_suffixes = [r"-mp-\d+(?:\.\d+)?", r"-\d+(?:\.\d+)?", r"\d\d"]
    compiler_version_regex = r"(?<!clang version)\s?([0-9.]+)"
    compiler_version_argument = ("-dumpfullversion", "-dumpversion")

    def install(self, spec, prefix):
        # Create the minimal compiler that will fool `spack compiler find`
        mkdirp(prefix.bin)
        with open(prefix.bin.gcc, "w") as f:
            f.write('#!/bin/bash\necho "%s"' % str(spec.version))
        set_executable(prefix.bin.gcc)
