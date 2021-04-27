# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class ROrgHsEgDb(RPackage):
    """Genome wide annotation for Human

    Genome wide annotation for Human, primarily based on mapping using Entrez
    Gene identifiers."""

    homepage = "https://bioconductor.org/packages/org.Hs.eg.db/"
    url      = "https://www.bioconductor.org/packages/3.5/data/annotation/src/contrib/org.Hs.eg.db_3.4.1.tar.gz"

    version('3.12.0',
            sha256='48a1ab5347ec7a8602c555d9aba233102b61ffa2765826e5c8890ff0003249bb',
            url='https://www.bioconductor.org/packages/3.12/data/annotation/src/contrib/org.Hs.eg.db_3.12.0.tar.gz')
    version('3.8.2',
            sha256='a0a16b7428f9e3d6ba54ebf4e05cd97a7bd298510ec4cf46ed2bed3e8f80db02',
            url='https://www.bioconductor.org/packages/3.9/data/annotation/src/contrib/org.Hs.eg.db_3.8.2.tar.gz')
    version('3.4.1',
            sha256='0f87b3f1925a1d7007e5ad9200bdf511788bd1d7cb76f1121feeb109889c2b00',
            url='https://www.bioconductor.org/packages/3.5/data/annotation/src/contrib/org.Hs.eg.db_3.4.1.tar.gz')

    depends_on('r@2.7.0:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.37.4:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.43.1:', when='@3.8.2:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.51.3:', when='@3.12.0:', type=('build', 'run'))
