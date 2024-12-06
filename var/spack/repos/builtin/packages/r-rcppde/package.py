# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcppde(RPackage):
    """Global Optimization by Differential Evolution in C++.

    An efficient C++ based implementation of the 'DEoptim' function which
    performs global optimization by differential evolution. Its creation was
    motivated by trying to see if the old approximation "easier, shorter,
    faster: pick any two" could in fact be extended to achieving all three
    goals while moving the code from plain old C to modern C++. The initial
    version did in fact do so, but a good part of the gain was due to an
    implicit code review which eliminated a few inefficiencies which have since
    been eliminated in 'DEoptim'."""

    cran = "RcppDE"

    version("0.1.7", sha256="4a238ee97e574cb44b12e4962b9927dd811f087fc13fc777637ec6fe12bd86a0")
    version("0.1.6", sha256="c9386709f72cdc33505b3ac675c173013fe098434b7c21bc09eb625b529132c5")

    depends_on("cxx", type="build")  # generated

    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rcpparmadillo", type=("build", "run"))
