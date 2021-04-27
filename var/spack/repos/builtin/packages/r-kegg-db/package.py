# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RKeggDb(RPackage):
    """A set of annotation maps for KEGG

    A set of annotation maps for KEGG assembled using data from KEGG."""

    # NOTE: The KEGG.db package is deprecated

    homepage = "https://www.bioconductor.org/packages/KEGG.db/"
    url = "https://www.bioconductor.org/packages/release/data/annotation/src/contrib/KEGG.db_3.2.3.tar.gz"

    version('3.2.4',
            sha256='2e60d1b664cbd1491cc00ed13a22904706c5a4651150f70daca04bf3ba9ead88',
            url='https://bioconductor.org/packages/3.12/data/annotation/src/contrib/KEGG.db_3.2.4.tar.gz')
    version('3.2.3',
            sha256='02ea4630a3ec06a8d9a6151627c96d3f71dfc7e8857800bb5c0cdb6a838d6963',
            url='https://bioconductor.org/packages/3.10/data/annotation/src/contrib/KEGG.db_3.2.3.tar.gz')

    depends_on('r@2.7.0:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.34.3:', type=('build', 'run'))
