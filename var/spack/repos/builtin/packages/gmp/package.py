# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gmp(AutotoolsPackage, GNUMirrorPackage):
    """GMP is a free library for arbitrary precision arithmetic, operating
    on signed integers, rational numbers, and floating-point numbers."""

    homepage = "https://gmplib.org"
    gnu_mirror_path = "gmp/gmp-6.1.2.tar.bz2"

    license("LGPL-3.0-or-later OR GPL-2.0-or-later")

    version("6.3.0", sha256="ac28211a7cfb609bae2e2c8d6058d66c8fe96434f740cf6fe2e47b000d1c20cb")
    version("6.2.1", sha256="eae9326beb4158c386e39a356818031bd28f3124cf915f8c5b1dc4c7a36b4d7c")
    version("6.2.0", sha256="f51c99cb114deb21a60075ffb494c1a210eb9d7cb729ed042ddb7de9534451ea")
    version("6.1.2", sha256="5275bb04f4863a13516b2f39392ac5e272f5e1bb8057b18aec1c9b79d73d8fb2")
    version("6.1.1", sha256="a8109865f2893f1373b0a8ed5ff7429de8db696fc451b1036bd7bdf95bbeffd6")
    version("6.1.0", sha256="498449a994efeba527885c10405993427995d3f86b8768d8cdf8d9dd7c6b73e8")
    version("6.0.0a", sha256="7f8e9a804b9c6d07164cf754207be838ece1219425d64e28cfa3e70d5c759aaf")
    version("5.1.3", sha256="752079520b4690531171d0f4532e40f08600215feefede70b24fabdc6f1ab160")
    # Old version needed for a binary package in ghc-bootstrap
    version("4.3.2", sha256="936162c0312886c21581002b79932829aa048cfaf9937c6265aeaa14f1cd1775")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )
    variant("cxx", default=True, description="Enable C++ support")

    # avoid using register x18 on aarch64 machines to prevent segfaults
    # https://gmplib.org/repo/gmp/raw-rev/5f32dbc41afc
    patch("avoid-x18.diff", when="@6.2.1")

    # gmp's configure script seems to be broken; it sometimes misdetects
    # shared library support. Regenerating it fixes the issue.
    force_autoreconf = True

    def flag_handler(self, name, flags):
        # Work around macOS Catalina / Xcode 11 code generation bug
        # (test failure t-toom53, due to wrong code in mpn/toom53_mul.o)
        if self.spec.satisfies("os=catalina") and name == "cflags":
            flags.append("-fno-stack-check")
        # This flag is necessary for the Intel build to pass `make check`
        elif self.spec.satisfies("%intel") and name == "cxxflags":
            flags.append("-no-ftz")
        return (flags, None, None)

    def configure_args(self):
        args = self.enable_or_disable("cxx")
        args += self.enable_or_disable("libs")
        if self.spec.satisfies("libs=static"):
            args.append("--with-pic")
        return args
