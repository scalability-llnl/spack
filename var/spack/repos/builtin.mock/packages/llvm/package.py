# Copyright Spack Project Developers. See COPYRIGHT file for details.
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

    provides("c", "cxx", when="+clang")

    c_names = ["clang"]
    cxx_names = ["clang++"]
    fortran_names = ["flang"]

    def install(self, spec, prefix):
        # Create the minimal compiler that will fool `spack compiler find`
        mkdirp(prefix.bin)
        with open(prefix.bin.gcc, "w", encoding="utf-8") as f:
            f.write('#!/bin/bash\necho "%s"' % str(spec.version))
        set_executable(prefix.bin.gcc)

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("c", None)
        result = None
        if "+clang" in self.spec:
            result = os.path.join(self.spec.prefix.bin, "clang")
        return result

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("cxx", None)
        result = None
        if "+clang" in self.spec:
            result = os.path.join(self.spec.prefix.bin, "clang++")
        return result

    @property
    def fortan(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("fc", None)
        result = None
        if "+flang" in self.spec:
            result = os.path.join(self.spec.prefix.bin, "flang")
        return result
