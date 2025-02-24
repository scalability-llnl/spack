# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDotcall64(RPackage):
    """Enhanced Foreign Function Interface Supporting Long
    Vectors.

    Provides .C64(), which is an enhanced version of .C() and .Fortran() from
    the foreign function interface. .C64() supports long vectors, arguments of
    type 64-bit integer, and provides a mechanism to avoid unnecessary copies
    of read-only and write-only arguments. This makes it a convenient and fast
    interface to C/C++ and Fortran code."""

    cran = "dotCall64"

    version("1.1-1", sha256="21b8d7d747c07aaf8a82d61ec98fe0539afcaa5a565d9c2fc55be65b6af2c91b")
    version("1.0-2", sha256="e0c7728aebbea5ebf06dfeefae4fc0a240e6dde7c2bf13f2ed041b91d337a4ac")
    version("1.0-1", sha256="f10b28fcffb9453b1d8888a72c8fd2112038b5ac33e02a481492c7bd249aa5c6")
    version("1.0-0", sha256="69318dc6b8aecc54d4f789c8105e672198363b395f1a764ebaeb54c0473d17ad")

    depends_on("r@3.1:", type=("build", "run"))
