# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLavaan(RPackage):
    """Latent Variable Analysis:

    Fit a variety of latent variable models, including confirmatory factor
    analysis, structural equation modeling and latent growth curve models."""

    homepage = "https://lavaan.ugent.be/"
    cran     = "lavaan"

    version('0.6-8', sha256='40e204909100b7338619ae23cd87e0a4058e581c286da2327f36dbb3834b84a2')

    depends_on('r@3.4:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mnormt', type=('build', 'run'))
    depends_on('r-pbivnorm', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
