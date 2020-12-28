# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCodex(RPackage):
    """A normalization and copy number variation calling procedure for whole
    exome DNA sequencing data. CODEX relies on the availability of multiple
    samples processed using the same sequencing pipeline for normalization, and
    does not require matched controls. The normalization model in CODEX
    includes terms that specifically remove biases due to GC content, exon
    length and targeting and amplification efficiency, and latent systemic
    artifacts. CODEX also includes a Poisson likelihood-based recursive
    segmentation procedure that explicitly models the count-based exome
    sequencing data."""

    homepage = "http://www.bioconductor.org/packages/release/bioc/html/CODEX.html"
    git      = "https://git.bioconductor.org/packages/CODEX"

    version('1.18.0', commit='9a95cccc7ff3fe587636317e21e39a07dddf80bc')

    depends_on('r@3.2.3:', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-bsgenome-hsapiens-ucsc-hg19', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
