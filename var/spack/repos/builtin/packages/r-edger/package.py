# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REdger(RPackage):
    """Empirical Analysis of Digital Gene Expression Data in R.

       Differential expression analysis of RNA-seq expression profiles with
       biological replication. Implements a range of statistical methodology
       based on the negative binomial distributions, including empirical Bayes
       estimation, exact tests, generalized linear models and quasi-likelihood
       tests. As well as RNA-seq, it be applied to differential signal analysis
       of other types of genomic data that produce counts, including ChIP-seq,
       Bisulfite-seq, SAGE and CAGE."""

    homepage = "https://bioconductor.org/packages/edgeR"
    git      = "https://git.bioconductor.org/packages/edgeR.git"

    version('3.26.8', commit='836809e043535f2264e5db8b5c0eabcffe85613f')
    version('3.24.3', commit='d1260a2aeba67b9ab7a9b8b197b746814ad0716d')
    version('3.22.5', commit='44461aa0412ef4a0d955730f365e44fc64fe1902')
    version('3.20.9', commit='acbcbbee939f399673678653678cd9cb4917c4dc')
    version('3.18.1', commit='101106f3fdd9e2c45d4a670c88f64c12e97a0495')

    depends_on('r@2.15.0:', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-locfit', type=('build', 'run'))

    depends_on('r-limma@3.34.5:', when='@3.20.9:', type=('build', 'run'))
    depends_on('r-rcpp', when='@3.20.9:', type=('build', 'run'))

    depends_on('r@3.6.0:', when='@3.26.8:', type=('build', 'run'))
