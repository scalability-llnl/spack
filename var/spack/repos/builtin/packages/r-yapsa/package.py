# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RYapsa(RPackage):
    """Yet Another Package for Signature Analysis.

       This package provides functions and routines useful in the analysis of
       somatic signatures (cf. L. Alexandrov et al., Nature 2013). In
       particular, functions to perform a signature analysis with known
       signatures (LCD = linear combination decomposition) and a signature
       analysis on stratified mutational catalogue (SMC = stratify mutational
       catalogue) are provided."""

    homepage = "https://bioconductor.org/packages/YAPSA"
    git      = "https://git.bioconductor.org/packages/YAPSA.git"

    version('1.10.0', commit='06af18e424868eb0f0be6c80e90cbab1eabf3d73')
    version('1.8.0', commit='402f3f7774fdf8afc7883579ad651c26df0f8fdb')
    version('1.6.0', commit='2455d272b076835ddb36ad21c01ef15af66abc36')
    version('1.4.0', commit='6f24150a0689d5215983975ece96c8c205923c72')
    version('1.2.0', commit='320809b69e470e30a777a383f8341f93064ec24d')

    depends_on('r@3.6.0:3.6.9', when='@1.10.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.8.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.6.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.4.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.2.0', type=('build', 'run'))

    depends_on('r-circlize', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-complexheatmap', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-corrplot', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-dendextend', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-genomeinfodb', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-genomicranges', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-getoptlong', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-ggplot2', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-gridextra', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-gtrellis', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-keggrest', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-lsei', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-pmcmr', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-reshape2', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-somaticsignatures', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-variantannotation', when='@1.2.0:', type=('build', 'run'))
