# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Llvm(Package, CompilerPackage):
    """Simple compiler package."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/gcc-1.0.tar.gz"

    version("18.1.8", md5="0123456789abcdef0123456789abcdef")

    variant(
        "clang", default=True, description="Build the LLVM C/C++/Objective-C compiler frontend"
    )

    c_names = ["clang"]
    cxx_names = ["clang++"]
    fortran_names = ["flang"]

    def install(self, spec, prefix):
        # Create the minimal compiler that will fool `spack compiler find`
        mkdirp(prefix.bin)
        with open(prefix.bin.gcc, "w") as f:
            f.write('#!/bin/bash\necho "%s"' % str(spec.version))
        set_executable(prefix.bin.gcc)
