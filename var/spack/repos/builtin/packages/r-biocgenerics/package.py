# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocgenerics(RPackage):
    """S4 generic functions used in Bioconductor.

       The package defines S4 generic functions used in Bioconductor."""

    homepage = "https://bioconductor.org/packages/BiocGenerics"
    git      = "https://git.bioconductor.org/packages/BiocGenerics.git"

    version('0.34.0', commit='f7c2020')
    version('0.30.0', commit='fc7c3af4a5635a30988a062ed09332c13ca1d1a8')
    version('0.28.0', commit='041fc496504f2ab1d4d863fffb23372db214394b')
    version('0.26.0', commit='5b2a6df639e48c3cd53789e0b174aec9dda6b67d')
    version('0.24.0', commit='3db111e8c1f876267da89f4f0c5406a9d5c31cd1')
    version('0.22.1', commit='9c90bb8926885289d596a81ff318ee3745cbb6ad')

    depends_on('r@3.6.0:', when='@0.30.0:', type=('build', 'run'))
