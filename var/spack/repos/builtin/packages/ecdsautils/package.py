# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ecdsautils(CMakePackage):
    """Tiny collection of programs used for ECDSA."""

    homepage = "https://github.com/freifunk-gluon/"
    url      = "https://github.com/freifunk-gluon/ecdsautils/archive/v0.3.2.tar.gz"

    version('0.3.2', sha256='a828417c985ccfc623bb613e92ccc8af6c6f24a5bcab8b112b90c033a816204f')
    version('0.3.1', sha256='4b6efe7802a089e8d64194c954a8f9981ff516b922b40d51e6c7ba565274a87a')

    depends_on('libuecc', type='build')
