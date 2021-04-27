# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGamlss(RPackage):
    """Generalised Additive Models for Location Scale and Shape

    Functions for fitting the Generalized Additive Models for Location Scale
    and Shape introduced by Rigby and Stasinopoulos (2005),
    <doi:10.1111/j.1467-9876.2005.00510.x>. The models use a distributional
    regression approach where all the parameters of the conditional
    distribution of the response variable are modelled using explanatory
    variables."""

    homepage = "https://cloud.r-project.org/package=gamlss"
    url      = "https://cloud.r-project.org/src/contrib/gamlss_5.1-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gamlss/"

    version('5.2-0', sha256='d3927547109064cbe7b0f955144f53204b5dc86c6b2dbc8f0551a74140ab02e1')
    version('5.1-4', sha256='e2fc36fe6ca3a69d69cdafd9533a4ff35090fdfb01df126f6a49156f4aa3376c')
    version('5.1-3', sha256='d37d121bc2acdbacc20cea04a1ed4489a575079e2a7b17b4a9823ee283857317')
    version('5.1-2', sha256='0d404e74768a8f98c6a5e9a48bd2cf4280125831a5dcd8c7f7b57922f57e016b')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-gamlss-data@5.0-0:', type=('build', 'run'))
    depends_on('r-gamlss-dist@4.3.1:', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
