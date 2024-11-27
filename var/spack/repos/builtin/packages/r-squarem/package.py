# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSquarem(RPackage):
    """Squared Extrapolation Methods for Accelerating EM-Like Monotone
    Algorithms.

    Algorithms for accelerating the convergence of slow, monotone sequences
    from smooth, contraction mapping such as the EM algorithm. It can be used
    to accelerate any smooth, linearly convergent acceleration scheme.  A
    tutorial style introduction to this package is available in a vignette on
    the CRAN download page or, when the package is loaded in an R session, with
    vignette("SQUAREM"). Refer to the J Stat Software article:
    <doi:10.18637/jss.v092.i07>."""

    cran = "SQUAREM"

    version("2021.1", sha256="66e5e18ca29903e4950750bbd810f0f9df85811ee4195ce0a86d939ba8183a58")
    version("2017.10-1", sha256="9b89905b436f1cf3faa9e3dabc585a76299e729e85ca659bfddb4b7cba11b283")

    depends_on("r@3.0:", type=("build", "run"))
