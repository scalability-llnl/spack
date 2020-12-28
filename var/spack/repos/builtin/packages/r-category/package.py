# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCategory(RPackage):
    """Category Analysis.

       A collection of tools for performing category (gene set enrichment)
       analysis."""

    homepage = "https://bioconductor.org/packages/Category"
    git      = "https://git.bioconductor.org/packages/Category.git"

    version('2.50.0', commit='d96f0b29cb778f6697b44d7ba7b0abd7086074a9')
    version('2.48.1', commit='941819a3d9dd129f47b4ea00fa74032e405be3a5')
    version('2.46.0', commit='c8aeee4dee3fb120f25e0647dd06e895a3ffbc2a')
    version('2.44.0', commit='eaba50c1a801ba7983e6ffdf41ab0fc9cfe5a626')
    version('2.42.1', commit='382c817a2371671a72f8f949dfb4050361ebabcd')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-rbgl', type=('build', 'run'))
    depends_on('r-gseabase', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-annotate', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
