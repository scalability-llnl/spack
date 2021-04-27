# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RPinfsc50(RPackage):
    """Sequence ('FASTA'), Annotation ('GFF') and Variants ('VCF') for 17
    Samples of 'P. Infestans" and 1 'P. Mirabilis'

    Genomic data for the plant pathogen "Phytophthora infestans." It includes
    a variant file ('VCF'), a sequence file ('FASTA') and an annotation file
    ('GFF'). This package is intended to be used as example data for packages
    that work with genomic data."""

    homepage = "https://cloud.r-project.org/web/packages/pinfsc50/index.html"
    cran     = "pinfsc50"

    maintainers = ['dorton21']

    version('1.2.0', sha256='ed1fe214b9261feef8abfbf724c2bd9070d68e99a6ea95208aff2c57bbef8794')

    depends_on('r@3.2.1:', type=('build', 'run'))
