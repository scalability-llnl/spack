# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMnormt(RPackage):
    """The Multivariate Normal and t Distributions, and Their Truncated
    Versions.

    Functions are provided for computing the density and the distribution
    function of multivariate normal and "t" random variables, and for
    generating random vectors sampled from these distributions.  Probabilities
    are computed via non-Monte Carlo methods; different routines are used in
    the case d=1, d=2, d>2, if d denotes the number of dimensions."""

    cran = "mnormt"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("2.1.1", sha256="95fca70378af0afd5a388982ba5528f5b27e02157eeb9940a0a9762d11511308")
    version("2.0.2", sha256="5c6aa036d3f1035ffe8f9a8e95bb908b191b126b016591cf893c50472851f334")
    version("1.5-5", sha256="ff78d5f935278935f1814a69e5a913d93d6dd2ac1b5681ba86b30c6773ef64ac")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("r@2.2.0:", type=("build", "run"))
    depends_on("r-tmvnsim@1.0-2:", type=("build", "run"), when="@2.0.2")
