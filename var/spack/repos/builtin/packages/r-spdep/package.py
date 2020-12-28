# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpdep(RPackage):
    """A collection of functions to create spatial weights matrix objects from
    polygon contiguities, from point patterns by distance and tessellations,
    for summarizing these objects, and for permitting their use in spatial
    data analysis, including regional aggregation by minimum spanning tree;
    a collection of tests for spatial autocorrelation, including global
    Moran's I, APLE, Geary's C, Hubert/Mantel general cross product statistic,
    Empirical Bayes estimates and AssunasReis Index, Getis/Ord G and
    multicoloured join count statistics, local Moran's I and Getis/Ord G,
    saddlepoint approximations and exact tests for global and local Moran's I;
    and functions for estimating spatial simultaneous autoregressive (SAR) lag
    and error models, impact measures for lag models, weighted and unweighted
    SAR and CAR spatial regression models, semi-parametric and Moran
    eigenvector spatial filtering, GM SAR error models, and generalized spatial
    two stage least squares models."""

    homepage = "https://r-forge.r-project.org/projects/spdep"
    url      = "https://cloud.r-project.org/src/contrib/spdep_0.6-13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spdep"

    version('1.1-2', sha256='ba0ca3a0ad6b9cc1dc46cadd9e79259949ad38c88f738e98e482d6c06640b31a')
    version('1.0-2', sha256='6f9efa4347d5c13b49922b75481ac403431c3c76a65a109af29954aa7bb138b2')
    version('0.6-13', sha256='ed345f4c7ea7ba064b187eb6b25f0ac46f17616f3b56ab89978935cdc67df1c4')

    depends_on('r@3.0.0:', when='@:0.7-7', type=('build', 'run'))
    depends_on('r@3.3.0:', when='@0.7-8:', type=('build', 'run'))
    depends_on('r-sp@1.0:', type=('build', 'run'))
    depends_on('r-learnbayes', type=('build', 'run'))
    depends_on('r-deldir', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-gmodels', type=('build', 'run'))
    depends_on('r-expm', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-boot@1.3-1:', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-spdata@0.2.6.0:', when='@1.0-2:', type=('build', 'run'))
    depends_on('r-sf', when='@1.0-2:', type=('build', 'run'))
