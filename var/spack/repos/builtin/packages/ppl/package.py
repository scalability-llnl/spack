# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ppl(Package):
    """The Parma Polyhedra Library (PPL) provides numerical
    abstractions especially targeted at applications in the field of
    analysis and verification of complex systems. These abstractions
    include convex polyhedra, some special classes of polyhedra shapes
    that offer interesting complexity/precision tradeoffs, and grids
    which represent regularly spaced points that satisfy a set of
    linear congruence relations. The library also supports finite
    powersets and products of polyhedra and grids, a mixed integer
    linear programming problem solver using an exact-arithmetic
    version of the simplex algorithm, a parametric integer programming
    solver, and primitives for termination analysis via the automatic
    synthesis of linear ranking functions."""

    homepage = "https://bugseng.com/products/ppl/"
    url = "http://bugseng.com/products/ppl/download/ftp/releases/1.1/ppl-1.1.tar.gz"

    license("GPL-3.0-or-later")

    version("1.2", sha256="6bc36dd4a87abc429d8f9c00c53e334e5041a9b0857cfc00dbad6ef14294aac8")
    version("1.1", sha256="46f073c0626234f0b1a479356c0022fe5dc3c9cf10df1a246c9cde81f7cf284d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("gmp")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix, "--with-gmp=%s" % spec["gmp"].prefix)
        make()
        make("install")
