# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMcmc(RPackage):
    """Markov Chain Monte Carlo.

    Simulates continuous distributions of random vectors using Markov chain
    Monte Carlo (MCMC). Users specify the distribution by an R function that
    evaluates the log unnormalized density. Algorithms are random walk
    Metropolis algorithm (function metrop), simulated tempering (function
    temper), and morphometric random walk Metropolis (Johnson and Geyer, 2012,
    <doi:10.1214/12-AOS1048>, function morph.metrop), which achieves geometric
    ergodicity by change of variable."""

    cran = "mcmc"

    license("MIT")

    version("0.9-8", sha256="6a06440d4b58e8a7f122747d92046ff40da4bb58a20bf642228a648a0c826ea7")
    version("0.9-7", sha256="b7c4d3d5f9364c67a4a3cd49296a61c315ad9bd49324a22deccbacb314aa8260")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@0.9-8:")
