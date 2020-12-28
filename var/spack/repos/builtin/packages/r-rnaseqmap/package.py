# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRnaseqmap(RPackage):
    """rnaSeq secondary analyses.

       The rnaSeqMap library provides classes and functions to analyze the RNA-
       sequencing data using the coverage profiles in multiple samples at a
       time"""

    homepage = "https://bioconductor.org/packages/rnaSeqMap"
    git      = "https://git.bioconductor.org/packages/rnaSeqMap.git"

    version('2.42.0', commit='3a3a1030cc38d79d04536e0ab16114e4fa6721cf')
    version('2.40.1', commit='c122d645b3503fb1a061f5515e4f8cf2863b3ba3')
    version('2.38.0', commit='5eb9583bfacd375161739a8ae6057204487f8b9e')
    version('2.36.0', commit='69c46fa467be0ac30776ede85a521f7622539b7e')
    version('2.34.0', commit='7881bc00600ed824ac437edf3cfba35573261e46')

    depends_on('r@2.11.0:', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-deseq', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
