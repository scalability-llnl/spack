# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCoda(RPackage):
    """Output Analysis and Diagnostics for MCMC.

    Provides functions for summarizing and plotting the output from Markov
    Chain Monte Carlo (MCMC) simulations, as well as diagnostic tests of
    convergence to the equilibrium distribution of the Markov chain."""

    cran = "coda"

    license("GPL-2.0-or-later")

    version("0.19-4.1", sha256="f4b451d86fbb56ff9ade043ddd6b0944368c37d0dad12d02837750ecdc708ad6")
    version("0.19-4", sha256="422d3cfd34797a3631e9c4812431940599c0ca4bb9937797bed07b7b1d6fe58f")
    version("0.19-3", sha256="d3df1fc848bcf1af8fae13d61eeab60e99a3d4b4db384bec4326f909f502c5d6")
    version("0.19-2", sha256="678a7e6a87a2723089daeb780ea37ac3d4319b37eabe26928ea3fa9c9b1eda0d")
    version("0.19-1", sha256="d41ff5731da6805170769dba75dd011ab33f916d15b2336001f279e21a524491")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
