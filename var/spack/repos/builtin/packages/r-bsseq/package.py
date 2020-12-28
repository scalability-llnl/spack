# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBsseq(RPackage):
    """A collection of tools for analyzing and visualizing bisulfite sequencing
    data."""

    homepage = "https://github.com/kasperdanielhansen/bsseq"
    git      = "https://git.bioconductor.org/packages/bsseq"

    version('1.24.4', commit='8fe7a03')
    version('1.22.0', commit='d4f7301')
    version('1.20.0', commit='07e398b')

    depends_on('r@3.5:', type=('build', 'run'))

    depends_on('r-biocgenerics', type=('build', 'run'))

    depends_on('r-genomicranges@1.29.14:', type=('build', 'run'))
    depends_on('r-genomicranges@1.33.6:', when='@1.24.4:', type=('build', 'run'))

    depends_on('r-summarizedexperiment@1.9.18:', type=('build', 'run'))
    depends_on('r-summarizedexperiment@1.17.4:', when='@1.24.4:', type=('build', 'run'))

    depends_on('r-iranges@2.11.16:', type=('build', 'run'))
    depends_on('r-iranges@2.22.2:', when='@1.24.4:', type=('build', 'run'))

    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-locfit', type=('build', 'run'))
    depends_on('r-gtools', type=('build', 'run'))
    depends_on('r-data-table@1.11.8:', type=('build', 'run'))

    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-s4vectors@0.23.11:', when='@1.22.0:', type=('build', 'run'))
    depends_on('r-s4vectors@0.25.14:', when='@1.24.4', type=('build', 'run'))

    depends_on('r-r-utils@2.0.0:', type=('build', 'run'))
    depends_on('r-delayedmatrixstats@1.5.2:', type=('build', 'run'))
    depends_on('r-permute', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-delayedarray@0.9.8:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-bsgenome', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-hdf5array@1.11.9:', type=('build', 'run'))
    depends_on('r-rhdf5', type=('build', 'run'))
    depends_on('r-beachmat', type=('build', 'run'))
