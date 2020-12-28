# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGoseq(RPackage):
    """Gene Ontology analyser for RNA-seq and other length biased data.

       Detects Gene Ontology and/or other user defined categories which are
       over/under represented in RNA-seq data"""

    homepage = "https://bioconductor.org/packages/goseq"
    git      = "https://git.bioconductor.org/packages/goseq.git"

    version('1.36.0', commit='26c9f7de18889afeee1b571ca1c4ab4d2877ab80')
    version('1.34.1', commit='bad217b42cc34423698fbcf701d4e3591aac4474')
    version('1.32.0', commit='32fcbe647eea17d7d0d7a262610811502c421d36')
    version('1.30.0', commit='fa8cafe0766ed0b6a97a4ed3374a709ed9d1daf1')
    version('1.28.0', commit='ed0ce332a8972618d740d8a93711dff994657738')

    depends_on('r@2.11.0:', type=('build', 'run'))
    depends_on('r-biasedurn', type=('build', 'run'))
    depends_on('r-genelendatabase@1.9.2:', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
