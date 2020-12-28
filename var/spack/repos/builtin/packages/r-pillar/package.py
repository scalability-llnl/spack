# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPillar(RPackage):
    """Provides a 'pillar' generic designed for formatting columns of data
       using the full range of colours provided by modern terminals."""

    homepage = "https://cloud.r-project.org/package=pillar"
    url      = "https://cloud.r-project.org/src/contrib/pillar_1.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pillar"

    version('1.4.2', sha256='bababb76b6db06dc32ccd947dbad6c164a1749ff5b558c6783ad03570f010825')
    version('1.4.1', sha256='f571ca7a3ef0927747510b972da31a26da24b9da68990fe1bbc9d4ae58028c55')
    version('1.3.1', sha256='b338b55f956dd7134f379d39bb94dfb25e13cf27999d6a6e6dc9f292755acbf6')
    version('1.3.0', sha256='aed845ae4888be9a7340eed57536e3fe6cb46e89d905897fb9b0635797cfcae0')
    version('1.2.3', sha256='c81d1b5c6b55d789a6717dc3c7be1200eb0efbcfc5013db00d553d9cafd6f0e7')
    version('1.2.2', sha256='676d6e64754ce42c2789ca3521eeb576c873afc3b09adfdf2c97f03cbcddb8ce')
    version('1.2.1', sha256='6de997a43416f436039f2b8b47c46ea08d2508f8ad341e0e1fd878704a3dcde7')
    version('1.2.0', sha256='fd042b525b27e5f700e5299f50d25710501a4f35556b6a04b430776568962416')
    version('1.1.0', sha256='58a29e8d0d3a47150caf8cb1aba5dc5eca233ac8d4626f4b23beb8b5ae9003be')
    version('1.0.1', sha256='7b37189ab9ab0bbf2e6f49e9d5e678acb31500739d3c3ea2b5326b457716277d')
    version('1.0.0', sha256='7478d0765212c5f0333b8866231a6fe350393b7fa49840e6fed3516ac64540dc')

    depends_on('r-cli', type=('build', 'run'))
    depends_on('r-crayon@1.3.4:', type=('build', 'run'))
    depends_on('r-fansi', type=('build', 'run'))
    depends_on('r-rlang@0.3.0:', type=('build', 'run'))
    depends_on('r-utf8@1.1.0:', type=('build', 'run'))
    depends_on('r-vctrs', when='@1.4.0:', type=('build', 'run'))
