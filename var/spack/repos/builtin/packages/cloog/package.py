# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cloog(Package):
    """CLooG is a free software and library to generate code for
    scanning Z-polyhedra. That is, it finds a code (e.g. in C,
    FORTRAN...) that reaches each integral point of one or more
    parameterized polyhedra."""

    homepage = "http://www.cloog.org"
    url = "http://www.bastoul.net/cloog/pages/download/count.php3?url=./cloog-0.18.1.tar.gz"
    list_url = "http://www.bastoul.net/cloog/pages/download"

    version("0.18.4", sha256="325adf3710ce2229b7eeb9e84d3b539556d093ae860027185e7af8a8b00a750e")
    version("0.18.1", sha256="02500a4edd14875f94fe84cbeda4290425cb0c1c2474c6f75d75a303d64b4196")
    version("0.18.0", sha256="1c4aa8dde7886be9cbe0f9069c334843b21028f61d344a2d685f88cb1dcf2228")
    version("0.17.0", sha256="f265f5069830c03d2919a7673c0963495437d6d79a8cbd3474cde2d4e3291e04")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("gmp")
    depends_on("isl")

    def install(self, spec, prefix):
        configure(
            "--prefix=%s" % prefix,
            "--with-osl=no",
            "--with-isl=%s" % spec["isl"].prefix,
            "--with-gmp=%s" % spec["gmp"].prefix,
        )
        make()
        make("install")
