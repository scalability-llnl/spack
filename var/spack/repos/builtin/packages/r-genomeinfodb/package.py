# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenomeinfodb(RPackage):
    """Utilities for manipulating chromosome names, including modifying them to
       follow a particular naming style.

       Contains data and functions that define and allow translation between
       different chromosome sequence naming conventions (e.g., "chr1" versus
       "1"), including a function that attempts to place sequence names in
       their natural, rather than lexicographic, order."""

    homepage = "https://bioconductor.org/packages/GenomeInfoDb"
    git      = "https://git.bioconductor.org/packages/GenomeInfoDb.git"

    version('1.20.0', commit='ea771e3b429ef17fb912fb37333556c6f77f2265')
    version('1.18.2', commit='557b75ea7734749a2650d30f5c5d52c57a6bcc6f')
    version('1.16.0', commit='6543dad89bbc2c275010b329eb114b237fd712fa')
    version('1.14.0', commit='4978308a57d887b764cc4ce83724ca1758f580f6')
    version('1.12.3', commit='2deef3f0571b7f622483257bc22d2509ab5a0369')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.13.8:', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.25:', type=('build', 'run'))
    depends_on('r-iranges@1.99.26:', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-genomeinfodbdata', type=('build', 'run'))

    depends_on('r-s4vectors@0.17.25:', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-iranges@2.13.12:', when='@1.16.0:', type=('build', 'run'))
