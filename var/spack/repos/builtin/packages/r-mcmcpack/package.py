# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMcmcpack(RPackage):
    """Markov Chain Monte Carlo (MCMC) Package.

    Contains functions to perform Bayesian inference using posterior simulation
    for a number of statistical models. Most simulation is done in compiled C++
    written in the Scythe Statistical Library Version 1.0.3. All models return
    'coda' mcmc objects that can then be summarized using the 'coda' package.
    Some useful utility functions such as density functions, pseudo-random
    number generators for statistical distributions, a general purpose
    Metropolis sampling algorithm, and tools for visualization are provided."""

    cran = "MCMCpack"

    version("1.7-0", sha256="846073d710017ec1dc9a2b4616cb6aeb60ce04e3500a37214522818d34045def")
    version("1.6-3", sha256="cb14ba20690b31fd813b05565484c866425f072a5ad99a5cbf1da63588958db3")
    version("1.6-0", sha256="b5b9493457d11d4dca12f7732bd1b3eb1443852977c8ee78393126f13deaf29b")
    version("1.5-0", sha256="795ffd3d62bf14d3ecb3f5307bd329cd75798cf4b270ff0e768bc71a35de0ace")

    depends_on("r@3.6:", type=("build", "run"))
    depends_on("r-coda@0.11-3:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-mcmc", type=("build", "run"))
    depends_on("r-quantreg", type=("build", "run"))

    conflicts("%gcc@:3")
