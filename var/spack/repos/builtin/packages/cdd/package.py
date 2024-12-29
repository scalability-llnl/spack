# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cdd(Package):
    """The program cdd+ (cdd, respectively) is a C++ (ANSI C)
    implementation of the Double Description Method [MRTT53] for
    generating all vertices (i.e. extreme points) and extreme rays of
    a general convex polyhedron given by a system of linear
    inequalities"""

    homepage = "https://www.inf.ethz.ch/personal/fukudak/cdd_home/cdd.html"
    url = "https://www.cs.mcgill.ca/~fukuda/download/cdd/cdd-061a.tar.gz"

    license("GPL-2.0-or-later")

    version("0.61a", sha256="637a1909bbd8aa4d32667da08f9e9ac687bf7d3ef1b8af5bd227e91a3cd4019b")

    depends_on("c", type="build")  # generated

    depends_on("libtool", type="build")

    patch("Makefile.spack.patch")

    def url_for_version(self, version):
        url = "https://www.cs.mcgill.ca/~fukuda/download/cdd/cdd-{0}.tar.gz"
        return url.format(version.joined)

    def install(self, spec, prefix):
        # The Makefile isn't portable; use our own instead
        makeargs = ["-f", "Makefile.spack", f"PREFIX={prefix}"]
        make(*makeargs)
        make("install", *makeargs)
