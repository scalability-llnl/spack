# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RShinystan(RPackage):
    """Interactive Visual and Numerical Diagnostics and Posterior Analysis for
    Bayesian Models.

    A graphical user interface for interactive Markov chain Monte Carlo (MCMC)
    diagnostics and plots and tables helpful for analyzing a posterior sample.
    The interface is powered by the 'Shiny' web application framework from
    'RStudio' and works with the output of MCMC programs written in any
    programming language (and has extended functionality for 'Stan' models fit
    using the 'rstan' and 'rstanarm' packages)."""

    cran = "shinystan"

    license("GPL-3.0-or-later")

    version("2.6.0", sha256="a084856a2d66d8744f2c72e3e19ca35e600a508ed7ef1f7ebed8c7fc0738d529")
    version("2.5.0", sha256="45f9c552a31035c5de8658bb9e5d72da7ec1f88fbddb520d15fe701c677154a1")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-shiny@1.0.3:", type=("build", "run"))
    depends_on("r-bayesplot@1.5.0:", type=("build", "run"))
    depends_on("r-colourpicker", type=("build", "run"))
    depends_on("r-dt@0.2:", type=("build", "run"))
    depends_on("r-dygraphs@1.1.1.2:", type=("build", "run"))
    depends_on("r-ggplot2@2.1.1:", type=("build", "run"))
    depends_on("r-gridextra", type=("build", "run"))
    depends_on("r-gtools", type=("build", "run"))
    depends_on("r-markdown@0.7.4:", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-rstan@2.17.1:", type=("build", "run"))
    depends_on("r-shinyjs@0.6.0:", type=("build", "run"))
    depends_on("r-shinythemes@1.0.1:", type=("build", "run"))
    depends_on("r-threejs@0.2.1:", type=("build", "run"))
    depends_on("r-xtable", type=("build", "run"))
    depends_on("r-xts@0.9-7:", type=("build", "run"))

    depends_on("r-rsconnect@0.4.2:", type=("build", "run"), when="@:2.5.0")
