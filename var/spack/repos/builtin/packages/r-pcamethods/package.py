# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPcamethods(RPackage):
    """A collection of PCA methods.

       Provides Bayesian PCA, Probabilistic PCA, Nipals PCA, Inverse Non-Linear
       PCA and the conventional SVD PCA. A cluster based method for missing
       value estimation is included for comparison. BPCA, PPCA and NipalsPCA
       may be used to perform PCA on incomplete data as well as for accurate
       missing value estimation. A set of methods for printing and plotting the
       results is also provided. All PCA methods make use of the same data
       structure (pcaRes) to provide a common interface to the PCA results.
       Initiated at the Max-Planck Institute for Molecular Plant Physiology,
       Golm, Germany."""

    homepage = "https://bioconductor.org/packages/pcaMethods"
    git      = "https://git.bioconductor.org/packages/pcaMethods.git"

    version('1.76.0', commit='5db995330ced37dfd5ddad6ad1d90b4815d3127a')
    version('1.74.0', commit='1b8f0a5cdfe3664119d0d7e926a2e0fe7320133c')
    version('1.72.0', commit='1bb8c7d056645e62ee5179f6bb30b6594ebf3bfd')
    version('1.70.0', commit='3368fad48ea930775505fd26e4179d7714d633d8')
    version('1.68.0', commit='c8d7c93dcaf7ef728f3d089ae5d55771b320bdab')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-rcpp@0.11.3:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
