# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDmrcate(RPackage):
    """Methylation array and sequencing spatial analysis methods:

    De novo identification and extraction of differentially methylated regions
    (DMRs) from the human genome using Whole Genome Bisulfite Sequencing (WGBS)
    and Illumina Infinium Array (450K and EPIC) data. Provides functionality
    for filtering probes possibly confounded by SNPs and cross-hybridisation.
    Includes GRanges generation and plotting functions."""

    bioc     = "DMRcate"

    version('2.4.1', commit='bc6242a0291a9b997872f575a4417d38550c9550')

    depends_on('r@3.6.0:', type=('build', 'run'))
    depends_on('r-minfi', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-experimenthub', type=('build', 'run'))
    depends_on('r-bsseq', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-dss', type=('build', 'run'))
    depends_on('r-missmethyl', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-gviz', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
