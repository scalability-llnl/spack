# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RChipseq(RPackage):
    """A package for analyzing chipseq data

    Tools for helping process short read data for chipseq experiments"""

    homepage = "https://bioconductor.org/packages/release/bioc/html/chipseq.html"
    git      = "https://git.bioconductor.org/packages/chipseq"

    maintainers = ['dorton21']

    version('1.40.0', commit='84bcbc0b7ad732730b5989a308f1624a6a358df1')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.1.0:', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.25:', type=('build', 'run'))
    depends_on('r-iranges@2.13.12:', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.8:', type=('build', 'run'))
    depends_on('r-shortread', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
