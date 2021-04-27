# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRepr(RPackage):
    """Serializable Representations

    String and binary representations of objects for several formats and
    mime types."""

    homepage = "https://github.com/IRkernel/repr"
    url      = "https://cloud.r-project.org/src/contrib/repr_0.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/repr"

    version('1.1.0', sha256='743fe018f9e3e54067a970bc38b6b8c0c0498b43f88d179ac4a959c2013a5f96')
    version('1.0.1', sha256='ecde22c17fd800e1ff5c2b2962689119aa486fba40fbc6f2c50e8d4cc61bc44b')
    version('1.0.0', sha256='98b2eb1058c1cb2caa8f98708b63726f5564b45de03d38b95ff6b963a8261f49')
    version('0.9', sha256='24cac6e98f2a7e5483cf87aaffcb37611702099b63d3783e319441b4ecd0264b')

    depends_on('r@3.0.1:', type=('build', 'run'))
    depends_on('r-htmltools', when='@0.13:', type=('build', 'run'))
    depends_on('r-jsonlite', when='@0.19.1:', type=('build', 'run'))
    depends_on('r-pillar@1.4.0:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-base64enc', when='@0.13:', type=('build', 'run'))
