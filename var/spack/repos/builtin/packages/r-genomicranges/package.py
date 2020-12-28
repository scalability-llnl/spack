# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenomicranges(RPackage):
    """Representation and manipulation of genomic intervals.

       The ability to efficiently represent and manipulate genomic annotations
       and alignments is playing a central role when it comes to analyzing
       high-throughput sequencing data (a.k.a. NGS data). The GenomicRanges
       package defines general purpose containers for storing and manipulating
       genomic intervals and variables defined along a genome. More specialized
       containers for representing and manipulating short alignments against a
       reference genome, or a matrix-like summarization of an experiment, are
       defined in the GenomicAlignments and SummarizedExperiment packages,
       respectively. Both packages build on top of the GenomicRanges
       infrastructure."""

    homepage = "https://bioconductor.org/packages/GenomicRanges"
    git      = "https://git.bioconductor.org/packages/GenomicRanges.git"

    version('1.36.1', commit='418e7e5647dd54d81b804455ddfcbc027fd0164a')
    version('1.34.0', commit='ebaad5ca61abb67c2c30c132e07531ba4257bccd')
    version('1.32.7', commit='4c56dc836dbfd0d228dc810e8d401811cdbc267c')
    version('1.30.3', commit='e99979054bc50ed8c0109bc54563036c1b368997')
    version('1.28.6', commit='197472d618f3ed04c795dc6ed435500c29619563')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.21.2:', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.47:', type=('build', 'run'))
    depends_on('r-iranges@2.9.11:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.11.5:', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))

    depends_on('r-iranges@2.11.16:', when='@1.30.3:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.13.1:', when='@1.30.3:', type=('build', 'run'))

    depends_on('r-biocgenerics@0.25.3:', when='@1.32.7:', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.32:', when='@1.32.7:', type=('build', 'run'))
    depends_on('r-iranges@2.14.4:', when='@1.32.7:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.15.2:', when='@1.32.7:', type=('build', 'run'))
    depends_on('r-xvector@0.19.8:', when='@1.32.7:', type=('build', 'run'))

    depends_on('r-s4vectors@0.19.11:', when='@1.34.0:', type=('build', 'run'))
    depends_on('r-iranges@2.15.12:', when='@1.34.0:', type=('build', 'run'))

    depends_on('r-iranges@2.17.1:', when='@1.36.1:', type=('build', 'run'))
