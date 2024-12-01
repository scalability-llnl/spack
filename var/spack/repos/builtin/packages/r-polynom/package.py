# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPolynom(RPackage):
    """A collection of functions to implement a class for univariate polynomial
    manipulations."""

    cran = "polynom"

    license("GPL-2.0-only")

    version("1.4-1", sha256="bc1edb7bb16c8b299103f80a52ab8c5fc200cd07a9056578c1f672e9f5019278")
    version("1.4-0", sha256="c5b788b26f7118a18d5d8e7ba93a0abf3efa6603fa48603c70ed63c038d3d4dd")
