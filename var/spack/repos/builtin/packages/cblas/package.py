# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cblas(Package):
    """The BLAS (Basic Linear Algebra Subprograms) are routines that
    provide standard building blocks for performing basic vector and
    matrix operations."""

    homepage = "http://www.netlib.org/blas/#_cblas"

    # tarball has no version, but on the date below, this MD5 was correct.
    version(
        "2015-06-06",
        sha256="0f6354fd67fabd909baf57ced2ef84e962db58fae126e4f41b21dd4fec60a2a3",
        url="https://www.netlib.org/blas/blast-forum/cblas.tgz",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("blas")
    parallel = False

    def patch(self):
        mf = FileFilter("Makefile.in")

        mf.filter("^BLLIB =.*", "BLLIB = {0}".format(" ".join(self.spec["blas"].libs.libraries)))
        mf.filter("^CC =.*", "CC = cc")
        mf.filter("^FC =.*", "FC = fc")

    def install(self, spec, prefix):
        make("all")
        mkdirp(prefix.lib)
        mkdirp(prefix.include)

        # Rename the generated lib file to libcblas.a
        install("lib/cblas_LINUX.a", prefix.lib.join("libcblas.a"))
        install("include/cblas.h", prefix.include)
        install("include/cblas_f77.h", prefix.include)
