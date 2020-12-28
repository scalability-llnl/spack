# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Aria2(AutotoolsPackage):
    """An ultra fast download utility"""

    homepage = "https://aria2.github.io"
    url      = "https://github.com/aria2/aria2/releases/download/release-1.35.0/aria2-1.35.0.tar.gz"

    version('1.35.0', sha256='fd85589416f8246cefc4e6ba2fa52da54fdf11fd5602a2db4b6749f7c33b5b2d')
    version('1.34.0', sha256='ec4866985760b506aa36dc9021dbdc69551c1a647823cae328c30a4f3affaa6c')

    depends_on('libxml2')
    depends_on('libssh2')
    depends_on('libgcrypt')
    depends_on('zlib')
    depends_on('c-ares')
    depends_on('sqlite')
