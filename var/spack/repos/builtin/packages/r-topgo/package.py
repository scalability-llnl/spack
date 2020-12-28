# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTopgo(RPackage):
    """Enrichment Analysis for Gene Ontology.

       topGO package provides tools for testing GO terms while accounting for
       the topology of the GO graph. Different test statistics and different
       methods for eliminating local similarities and dependencies between GO
       terms can be implemented and applied."""

    homepage = "https://bioconductor.org/packages/topGO"
    git      = "https://git.bioconductor.org/packages/topGO.git"

    version('2.36.0', commit='c2f6c187b41c4aa44cc92ac781fdd878491a4019')
    version('2.34.0', commit='44cb5eaba515b365b7b2a8c22df0a45883db6b4d')
    version('2.32.0', commit='78ce3068fc06ae38d55219759fa177e2fcb3f596')
    version('2.30.1', commit='b1469ce1d198ccb73ef79ca22cab81659e16dbaa')
    version('2.28.0', commit='066a975d460046cce33fb27e74e6a0ebc33fd716')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.13.6:', type=('build', 'run'))
    depends_on('r-graph@1.14.0:', type=('build', 'run'))
    depends_on('r-biobase@2.0.0:', type=('build', 'run'))
    depends_on('r-go-db@2.3.0:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.7.19:', type=('build', 'run'))
    depends_on('r-sparsem@0.73:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
