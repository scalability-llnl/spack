# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXvector(RPackage):
    """Foundation of external vector representation and manipulation in
       Bioconductor.

       Provides memory efficient S4 classes for storing sequences "externally"
       (e.g. behind an R external pointer, or on disk)."""

    homepage = "https://bioconductor.org/packages/XVector"
    git      = "https://git.bioconductor.org/packages/XVector.git"

    version('0.24.0', commit='e5109cb2687724b9fddddf296c07a82bae4c551d')
    version('0.22.0', commit='b5e107a5fd719e18374eb836eb498b529afa4473')
    version('0.20.0', commit='a83a7ea01f6a710f0ba7d9fb021cfa795b291cb4')
    version('0.18.0', commit='27acf47282c9880b54d04dff46c1e50f0c87fa6b')
    version('0.16.0', commit='54615888e1a559da4a81de33e934fc0f1c3ad99f')

    depends_on('r@2.8.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.19.2:', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.13:', type=('build', 'run'))
    depends_on('r-iranges@2.9.18:', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))

    depends_on('r-s4vectors@0.15.14:', when='@0.18.0:', type=('build', 'run'))

    depends_on('r-s4vectors@0.17.24:', when='@0.20.0:', type=('build', 'run'))
    depends_on('r-iranges@2.13.16:', when='@0.20.0:', type=('build', 'run'))

    depends_on('r-s4vectors@0.19.15:', when='@0.22.0:', type=('build', 'run'))
    depends_on('r-iranges@2.15.12:', when='@0.22.0:', type=('build', 'run'))

    depends_on('r-s4vectors@0.21.13:', when='@0.24.0:', type=('build', 'run'))
