# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTmixclust(RPackage):
    """Time Series Clustering of Gene Expression with Gaussian Mixed-Effects
       Models and Smoothing Splines.

       Implementation of a clustering method for time series gene expression
       data based on mixed-effects models with Gaussian variables and non-
       parametric cubic splines estimation. The method can robustly account for
       the high levels of noise present in typical gene expression time series
       datasets."""

    homepage = "https://bioconductor.org/packages/TMixClust"
    git      = "https://git.bioconductor.org/packages/TMixClust.git"

    version('1.6.0', commit='9f5f78e52538d15f402c8f6e4c60f7212c7bc548')
    version('1.4.0', commit='a52fcae6e7a5dd41e7afbe128f35397e8bc8cb12')
    version('1.2.0', commit='0250c0b238f08077b5b9ff17c2f3b7633c67dc3c')
    version('1.0.1', commit='0ac800210e3eb9da911767a80fb5582ab33c0cad')

    depends_on('r@3.4:', type=('build', 'run'))
    depends_on('r-gss', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-flexclust', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-spem', type=('build', 'run'))
