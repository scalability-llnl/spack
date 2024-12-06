# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTruncdist(RPackage):
    """Truncated Random Variables.

    A collection of tools to evaluate probability density functions, cumulative
    distribution functions, quantile functions and random numbers for truncated
    random variables. These functions are provided to also compute the expected
    value and variance. Nadarajah and Kotz (2006) developed most of the
    functions. QQ plots can be produced. All the probability functions in the
    stats, stats4 and evd packages are automatically available for
    truncation."""

    cran = "truncdist"

    license("GPL-2.0-or-later")

    version("1.0-2", sha256="b848b68bdd983bd496fa7327632ffa8add8d2231229b8af5c8bc29d823e1300a")

    depends_on("r@2.0.1:", type=("build", "run"))
    depends_on("r-evd", type=("build", "run"))
