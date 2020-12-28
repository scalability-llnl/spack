# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGamlss(RPackage):
    """gamlss: Generalised Additive Models for Location Scale and Shape"""

    homepage = "https://cloud.r-project.org/package=gamlss"
    url      = "https://cloud.r-project.org/src/contrib/gamlss_5.1-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gamlss/"

    version('5.1-4', sha256='e2fc36fe6ca3a69d69cdafd9533a4ff35090fdfb01df126f6a49156f4aa3376c')
    version('5.1-3', sha256='d37d121bc2acdbacc20cea04a1ed4489a575079e2a7b17b4a9823ee283857317')
    version('5.1-2', sha256='0d404e74768a8f98c6a5e9a48bd2cf4280125831a5dcd8c7f7b57922f57e016b')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-gamlss-data@5.0-0:', type=('build', 'run'))
    depends_on('r-gamlss-dist@4.3.1:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
