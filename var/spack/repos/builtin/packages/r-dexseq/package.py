# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDexseq(RPackage):
    """Inference of differential exon usage in RNA-Seq

    The package is focused on finding differential exon usage using RNA-seq
    exon counts between samples with different experimental designs. It
    provides functions that allows the user to make the necessary
    statistical tests based on a model that uses the negative binomial
    distribution to estimate the variance between biological replicates
    and generalized linear models for testing. The package also provides
    functions for the visualization and exploration of the results."""

    homepage = "http://www.bioconductor.org/packages/release/bioc/html/DEXSeq.html"
    url      = "http://www.bioconductor.org/packages/release/bioc/src/contrib/DEXSeq_1.36.0.tar.gz"
    bioc     = "DEXSeq"

    maintainers = ['dorton21']

    version('1.36.0', sha256='111b107cd70f770d1c6f1d5d6d2e447eb61008398b14a390979c64d60559d271')

    depends_on('r@2.14:', type=('build', 'run'))
    depends_on('r-biomart', type=('build', 'run'))
    depends_on('r-hwriter', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-statmod', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-iranges@2.5.17:', type=('build', 'run'))
    depends_on('r-genomicranges@1.23.7:', type=('build', 'run'))
    depends_on('r-deseq2@1.9.11:', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-s4vectors@0.23.18:', type=('build', 'run'))
