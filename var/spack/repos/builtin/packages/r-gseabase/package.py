# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGseabase(RPackage):
    """Gene set enrichment data structures and methods.

       This package provides classes and methods to support Gene Set Enrichment
       Analysis (GSEA)."""

    homepage = "https://bioconductor.org/packages/GSEABase"
    git      = "https://git.bioconductor.org/packages/GSEABase.git"

    version('1.46.0', commit='edce83a9256a0c03206c2bce7c90ada0d90f6622')
    version('1.44.0', commit='7042ff64a98b05b9572231ee1b4f3ae4fc9c768e')
    version('1.42.0', commit='5e40ce0fdd4dc0cff7601b169bbf6aa1430ae33e')
    version('1.40.1', commit='3e5441708b80aab2c9642988bee709d5732831a6')
    version('1.38.2', commit='84c9f10c316163118ca990900a7a67555b96e75b')

    depends_on('r@2.6.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.13.8:', type=('build', 'run'))
    depends_on('r-biobase@2.17.8:', type=('build', 'run'))
    depends_on('r-annotate@1.45.3:', type=('build', 'run'))
    depends_on('r-graph@1.37.2:', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
