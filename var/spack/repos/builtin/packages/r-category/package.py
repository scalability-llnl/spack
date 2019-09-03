# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCategory(RPackage):
    """Category Analysis

       A collection of tools for performing category (gene set enrichment)
       analysis."""

    homepage = "https://bioconductor.org/packages/Category"
    git      = "https://git.bioconductor.org/packages/Category.git"

    version('2.50.0', commit='d96f0b29cb778f6697b44d7ba7b0abd7086074a9')
    version('2.48.1', commit='941819a3d9dd129f47b4ea00fa74032e405be3a5')
    version('2.46.0', commit='c8aeee4dee3fb120f25e0647dd06e895a3ffbc2a')
    version('2.44.0', commit='eaba50c1a801ba7983e6ffdf41ab0fc9cfe5a626')
    version('2.42.1', commit='382c817a2371671a72f8f949dfb4050361ebabcd')

    depends_on('r@3.6.0:3.6.9', when='@2.50.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.48.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.46.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.44.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.42.1', type=('build', 'run'))

    depends_on('r-annotate', when='@2.42.1:', type=('build', 'run'))
    depends_on('r-annotationdbi', when='@2.42.1:', type=('build', 'run'))
    depends_on('r-biobase', when='@2.42.1:', type=('build', 'run'))
    depends_on('r-biocgenerics', when='@2.42.1:', type=('build', 'run'))
    depends_on('r-dbi', when='@2.42.1:', type=('build', 'run'))
    depends_on('r-genefilter', when='@2.42.1:', type=('build', 'run'))
    depends_on('r-graph', when='@2.42.1:', type=('build', 'run'))
    depends_on('r-gseabase', when='@2.42.1:', type=('build', 'run'))
    depends_on('r-matrix', when='@2.42.1:', type=('build', 'run'))
    depends_on('r-rbgl', when='@2.42.1:', type=('build', 'run'))
