# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSuppdists(RPackage):
    """Supplementary Distributions.

    Ten distributions supplementing those built into R. Inverse Gauss,
    Kruskal-Wallis, Kendall's Tau, Friedman's chi squared, Spearman's rho,
    maximum F ratio, the Pearson product moment correlation coefficient,
    Johnson distributions, normal scores and generalized hypergeometric
    distributions."""

    cran = "SuppDists"

    version("1.1-9.7", sha256="6b5527e2635c0ff762eb7af8154704c85e66d7f79a9524089a5c98dfa94dab08")
    version("1.1-9.5", sha256="680b67145c07d44e200275e08e48602fe19cd99fb106c05422b3f4a244c071c4")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.3.0:", type=("build", "run"))
