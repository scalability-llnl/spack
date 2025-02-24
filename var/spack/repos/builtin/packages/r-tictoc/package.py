# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTictoc(RPackage):
    """Functions for timing R scripts, as well as implementations of Stack and
    List structures.

    This package provides the timing functions 'tic' and 'toc' that can be
    nested. One can record all timings while a complex script is running, and
    examine the values later. It is also possible to instrument the timing
    calls with custom callbacks. In addition, this package provides class
    'Stack', implemented as a vector, and class 'List', implemented as a list,
    both of which support operations 'push', 'pop', 'first', 'last' and
    'clear'."""

    cran = "tictoc"

    license("Apache-2.0 OR custom")

    version("1.2.1", sha256="8fcdb7c9a1e4b4817bcab654effd64dea6ec749a7901d4060d5b5c625fc88833")
    version("1.2", sha256="f05ea4b4142a90b0dc5d10356be3748625ef86bbd0e4399c56455654165ff20c")
    version("1.1", sha256="120f868ba276bda70c8edef5d6c092586cf73db0fa02eb5459d8f55350fb474d")
    version("1.0.1", sha256="a09a1535c417ddf6637bbbda5fca6edab6c7f7b252a64e57e99d4d0748712705")
    version("1.0", sha256="47da097c1822caa2d8e262381987cfa556ad901131eb96109752742526b2e2fe")

    depends_on("r@3.0.3:", type=("build", "run"), when="@1.0.1:")
    depends_on("r@3.0.3:4.0", type=("build", "run"), when="@1.0")
    depends_on("r@2.15:", type=("build", "run"), when="@1.1:")
