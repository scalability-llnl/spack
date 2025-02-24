# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dtc(MakefilePackage):
    """Device Tree Compiler (dtc) toolchain for working with device tree
    source and binary files and also libfdt, a utility library for reading
    and manipulating the binary format."""

    homepage = "https://github.com/dgibson/dtc"
    url = "https://github.com/dgibson/dtc/archive/refs/tags/v1.6.1.tar.gz"

    license("GPL-2.0-or-later")

    version("1.6.1", sha256="6401c9a0f577a270df4632bf0f3e5454ccc7a5ca3caefa67a3e1c29c9c6b8c60")

    depends_on("c", type="build")  # generated

    depends_on("bison", type="build")
    # Build error with flex 2.6.3
    #   (convert-dtsv0-lexer.lex.c:398: error: "yywrap" redefined)
    depends_on("flex@2.6.4:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("python", type="build")
    depends_on("libyaml", type=("build", "link"))

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("PREFIX =.*", "PREFIX = %s" % prefix)
        if self.spec.satisfies("%clang") or self.spec.satisfies("%fj"):
            makefile.filter(
                r"WARNINGS = -Wall", "WARNINGS = -Wall -Wno-unused-command-line-argument"
            )

        if self.spec.satisfies("platform=darwin"):
            libfdt_makefile = FileFilter("libfdt/Makefile.libfdt")
            libfdt_makefile.filter(
                r"LIBFDT_soname = .*", "LIBFDT_soname = libfdt.1.$(SHAREDLIB_EXT)"
            )

    @run_after("install")
    def darwin_fix(self):
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)
