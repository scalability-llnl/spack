# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSomaticsignatures(RPackage):
    """Somatic Signatures.

       The SomaticSignatures package identifies mutational signatures of single
       nucleotide variants (SNVs). It provides a infrastructure related to the
       methodology described in Nik-Zainal (2012, Cell), with flexibility in
       the matrix decomposition algorithms."""

    homepage = "https://bioconductor.org/packages/SomaticSignatures"
    git      = "https://git.bioconductor.org/packages/SomaticSignatures.git"

    version('2.20.0', commit='dbedc30d92b600b3a17de596ebe38d15982c70c6')
    version('2.18.0', commit='facccd67eee5202fcbe6ad32e667546546e7ccff')
    version('2.16.0', commit='4ae348d9fa096c0ec307df95149991edf6044977')
    version('2.14.0', commit='b12d24f86e96a7c6a17cbbad21ca14fa3aa7c60f')
    version('2.12.1', commit='932298c6877d076004de5541cec85a14e819517a')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-variantannotation', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-nmf', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-ggbio', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-pcamethods', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-proxy', type=('build', 'run'))
