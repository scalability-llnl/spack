# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RPaleotree(RPackage):
    """Provides tools for transforming, a posteriori
       time-scaling, and modifying phylogenies containing
       extinct (i.e. fossil) lineages"""

    homepage = "https://github.com/dwbapst/paleotree"
    url      = "https://cloud.r-project.org/src/contrib/paleotree_3.1.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/paleotree"

    version('3.3.0', sha256='f8f6b0228dd5290b251cad3a8626689442b5aa793d8f072c8c2c7813a063df90')
    version('3.1.3', sha256='4c1cc8a5e171cbbbd88f78914f86d5e6d144ae573816fbeeff2ab54a814ec614')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-ape@4.1:', type=('build', 'run'))
    depends_on('r-phangorn@2.0.0:', type=('build', 'run'))
    depends_on('r-phytools@0.6-00:', type=('build', 'run'))
    depends_on('r-jsonlite', when='@3.3.0:', type=('build', 'run'))
    depends_on('r-png', when='@3.3.0:', type=('build', 'run'))
    depends_on('r-rcurl', when='@3.3.0:', type=('build', 'run'))
