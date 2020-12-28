# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiostrings(RPackage):
    """Efficient manipulation of biological strings.

       Memory efficient string containers, string matching algorithms, and
       other utilities, for fast manipulation of large biological sequences or
       sets of sequences."""

    homepage = "https://bioconductor.org/packages/Biostrings"
    git      = "https://git.bioconductor.org/packages/Biostrings.git"

    version('2.52.0', commit='b78fe7c1f3cdbbb7affb1ca7164fe5a1f8b868f5')
    version('2.50.2', commit='025e734641a93f6c5d44243297cb4264ea0e34a2')
    version('2.48.0', commit='aa3599a7d259d658014d087b86d71ab1deb5f12b')
    version('2.46.0', commit='3bf6978c155498b50607d1bb471d1687d185a0fa')
    version('2.44.2', commit='e4a2b320fb21c5cab3ece7b3c6fecaedfb1e5200')

    depends_on('r@2.8.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.15.6:', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.13:', type=('build', 'run'))
    depends_on('r-iranges@2.9.18:', when='@2.44.2:2.46.0', type=('build', 'run'))
    depends_on('r-xvector@0.11.6:', type=('build', 'run'))

    depends_on('r-s4vectors@0.17.25:', when='@2.48.0:', type=('build', 'run'))
    depends_on('r-iranges@2.13.24:', when='@2.48.0', type=('build', 'run'))
    depends_on('r-xvector@0.19.8:', when='@2.48.0:', type=('build', 'run'))

    depends_on('r@3.5.0:', when='@2.50.2:', type=('build', 'run'))
    depends_on('r-xvector@0.21.4:', when='@2.50.2:', type=('build', 'run'))
    depends_on('r-iranges', when='@2.50.2:', type=('build', 'run'))

    depends_on('r-s4vectors@0.21.13:', when='@2.52.0:', type=('build', 'run'))
    depends_on('r-xvector@0.23.2:', when='@2.52.0:', type=('build', 'run'))
