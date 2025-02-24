# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBayesplot(RPackage):
    """Plotting for Bayesian Models.

    Plotting functions for posterior analysis, MCMC diagnostics, prior and
    posterior predictive checks, and other visualizations to support the
    applied Bayesian workflow advocated in Gabry, Simpson, Vehtari, Betancourt,
    and Gelman (2019) <doi:10.1111/rssa.12378>. The package is designed not
    only to provide convenient functionality for users, but also a common set
    of functions that can be easily used by developers working on a variety of
    R packages for Bayesian modeling, particularly (but not exclusively)
    packages interfacing with 'Stan'."""

    cran = "bayesplot"

    license("GPL-3.0-or-later")

    version("1.11.1", sha256="4f71e67391e0135acd3e890989b87025f3f8160242f532a8e1a0ed74ed0f3830")
    version("1.10.0", sha256="bb4cb92b1ae4cf8ae5f4b5cb092aba34af3d820d137e1f2265cca8f3e85113ff")
    version("1.9.0", sha256="0a81a4b99cf781334e57cfc3c469fad8b932a68204016a3bbca33cab4e2a1e43")
    version("1.8.1", sha256="d8d74201ea91fa5438714686ca22a947ec9375b6c12b0cfef010c57104b1aa2a")
    version("1.8.0", sha256="a605f9929e681593a3ef3ca9c836e713314994aaea00f359f71cfc42d151c948")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-dplyr@0.8.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.0.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.4.0:", type=("build", "run"), when="@1.11.0:")
    depends_on("r-ggridges", type=("build", "run"))
    depends_on("r-ggridges@0.5.5:", type=("build", "run"), when="@1.11.1:")
    depends_on("r-glue", type=("build", "run"))
    depends_on("r-posterior", type=("build", "run"), when="@1.9.0:")
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-rlang@0.3.0:", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-tibble@2.0.0:", type=("build", "run"), when="@1.9.0:")
    depends_on("r-tidyselect", type=("build", "run"))
    depends_on("pandoc@1.12.3:", when="@1.9.0:")
