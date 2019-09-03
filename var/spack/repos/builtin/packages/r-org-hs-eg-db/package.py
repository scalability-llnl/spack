# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ROrgHsEgDb(RPackage):
    """Genome wide annotation for Human, primarily based on mapping
    using Entrez Gene identifiers."""

    homepage = "https://bioconductor.org/packages/org.Hs.eg.db/"
    url      = "https://www.bioconductor.org/packages/3.5/data/annotation/src/contrib/org.Hs.eg.db_3.4.1.tar.gz"

    version('3.8.2', sha256='a0a16b7428f9e3d6ba54ebf4e05cd97a7bd298510ec4cf46ed2bed3e8f80db02',
            url='https://www.bioconductor.org/packages/3.9/data/annotation/src/contrib/org.Hs.eg.db_3.8.2.tar.gz')

    version('3.4.1', '0a987ef7d6167df70e91e6f48145e41c')

    depends_on('r@3.6.0:3.6.9', when='@3.8.2')
    depends_on('r@3.4.0:3.4.9', when='@3.4.1')

    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-annotationdbi@1.43.1:', when='@3.8.2', type=('build', 'run'))
