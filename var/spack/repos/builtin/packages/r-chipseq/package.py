# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RChipseq(RPackage):
    """A package for analyzing chipseq data"""

    homepage = "https://bioconductor.org/packages/release/bioc/html/chipseq.html"
    url      = "https://bioconductor.org/packages/release/bioc/src/contrib/chipseq_1.40.0.tar.gz"

    maintainers = ['dorton21']

    version('1.40.0', sha256='5b48721a9eae6ebaf57a57af13f76eb887925ea1a02906abeb6f67a588c0ff8a')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.1.0:', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.25:', type=('build', 'run'))
    depends_on('r-iranges@2.13.12:', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.8:', type=('build', 'run'))
    depends_on('r-shortread', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
