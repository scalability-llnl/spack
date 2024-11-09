# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class IntelOneapiCompilers(Package, CompilerPackage):
    """Simple compiler package."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/oneapi-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("3.0", md5="def0123456789abcdef0123456789abc")

    compiler_languages = ["c", "cxx", "fortran"]
    c_names = ["icx"]
    cxx_names = ["icpx"]
    fortran_names = ["ifx"]
    compiler_version_argument = "--version"
    compiler_version_regex = (
        r"(?:(?:oneAPI DPC\+\+(?:\/C\+\+)? Compiler)|(?:\(IFORT\))|(?:\(IFX\))) (\S+)"
    )

    @property
    def compiler_search_prefix(self):
        return self.prefix.foo.bar.baz.bin

    def install(self, spec, prefix):
        # Create the minimal compiler that will fool `spack compiler find`
        mkdirp(self.compiler_search_prefix)
        comp = self.compiler_search_prefix.icx
        if sys.platform == "win32":
            comp = comp + ".bat"
            comp_string = f"@echo off\necho oneAPI DPC++ Compiler {str(spec.version)}"
        else:
            comp_string = f'#!/bin/bash\necho "oneAPI DPC++ Compiler {str(spec.version)}"'
        with open(comp, "w") as f:
            f.write(comp_string)
        set_executable(comp)
