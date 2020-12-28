# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnnotationdbi(RPackage):
    """Manipulation of SQLite-based annotations in Bioconductor.

       Implements a user-friendly interface for querying SQLite-based
       annotation data packages."""

    homepage = "https://bioconductor.org/packages/AnnotationDbi"
    git      = "https://git.bioconductor.org/packages/AnnotationDbi.git"

    version('1.46.1', commit='ff260913741d0fcf9487eeb1f44a6c6968ced5b9')
    version('1.44.0', commit='ce191b08cfd612d014431325c26c91b11c5f13ac')
    version('1.42.1', commit='71085b47ea2e1ef929bebe8b17eb8e8a573f98e3')
    version('1.40.0', commit='e34dff07e10402eecbf95604a512bc1fc4edb127')
    version('1.38.2', commit='67d46facba8c15fa5f0eb47c4e39b53dbdc67c36')

    depends_on('r@2.7.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.15.10:', type=('build', 'run'))
    depends_on('r-biobase@1.17.0:', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.25:', type=('build', 'run'))

    depends_on('r-biocgenerics@0.23.1:', when='@1.40.0:', type=('build', 'run'))

    depends_on('r-biocgenerics@0.29.2:', when='@1.46.1:', type=('build', 'run'))
