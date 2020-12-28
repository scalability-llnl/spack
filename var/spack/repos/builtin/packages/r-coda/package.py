# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCoda(RPackage):
    """Provides functions for summarizing and plotting the output from
       Markov Chain Monte Carlo (MCMC) simulations, as well as
       diagnostic tests of convergence to the equilibrium distribution
       of the Markov chain."""

    homepage = "https://cloud.r-project.org/package=coda"
    url      = "https://cloud.r-project.org/src/contrib/coda_0.19-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/coda"

    version('0.19-3', sha256='d3df1fc848bcf1af8fae13d61eeab60e99a3d4b4db384bec4326f909f502c5d6')
    version('0.19-2', sha256='678a7e6a87a2723089daeb780ea37ac3d4319b37eabe26928ea3fa9c9b1eda0d')
    version('0.19-1', sha256='d41ff5731da6805170769dba75dd011ab33f916d15b2336001f279e21a524491')

    depends_on('r@2.14:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
