# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenelendatabase(RPackage):
    """Lengths of mRNA transcripts for a number of genomes.

       Length of mRNA transcripts for a number of genomes and gene ID formats,
       largely based on UCSC table browser"""

    homepage = "https://bioconductor.org/packages/geneLenDataBase"
    git      = "https://git.bioconductor.org/packages/geneLenDataBase.git"

    version('1.20.0', commit='70a1abed00ee68f7bfa07c42c011f9edae9915e4')
    version('1.18.0', commit='77db87e5a4819bf94761fabef0d2ff741a1c5d07')
    version('1.16.0', commit='c2a8b2359c6c59388853d6f6d15d71dffb17a198')
    version('1.14.0', commit='b456b3ffb04eaf335893fdec2bb10f6795dd7e08')
    version('1.12.0', commit='85d6536763c12850e6c01da9e2f9e0b9c07601fe')

    depends_on('r@2.11.0:', type=('build', 'run'))
    depends_on('r-rtracklayer', type=('build', 'run'))
    depends_on('r-genomicfeatures@1.3.15:', type=('build', 'run'))
