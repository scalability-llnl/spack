# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffycoretools(RPackage):
    """Functions useful for those doing repetitive analyses with Affymetrix
       GeneChips.

       Various wrapper functions that have been written to streamline the more
       common analyses that a core Biostatistician might see."""

    homepage = "https://bioconductor.org/packages/affycoretools"
    git      = "https://git.bioconductor.org/packages/affycoretools.git"

    version('1.56.0', commit='71eab04056a8d696470420a600b14900186be898')
    version('1.54.0', commit='1e1f9680bc3e1fa443f4a81ce5ab81349959b845')
    version('1.52.2', commit='2f98c74fad238b94c1e453b972524ab7b573b0de')
    version('1.50.6', commit='4be92bcb55d7bace2a110865b7530dcfac14e76e')
    version('1.48.0', commit='e0d52e34eead1ac45d3e60c59efd940e4889eb99')

    depends_on('r@3.6.0:3.6.9', when='@1.56.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.54.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.52.2', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.50.6', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.48.0', type=('build', 'run'))

    depends_on('r-affy', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-annotationdbi', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-biobase', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-biocgenerics', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-edger', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-gcrma', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-ggplot2', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-gostats', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-gplots', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-hwriter', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-lattice', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-limma', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-oligoclasses', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-reportingtools', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-rsqlite', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-s4vectors', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-xtable', when='@1.48.0:', type=('build', 'run'))

    depends_on('r-dbi', when='@1.50.6:', type=('build', 'run'))
