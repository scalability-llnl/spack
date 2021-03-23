# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Flac(AutotoolsPackage):
    """Encoder/decoder for the Free Lossless Audio Codec"""

    homepage = "https://xiph.org/flac/index.html"
    url      = "http://downloads.xiph.org/releases/flac/flac-1.3.2.tar.xz"

    version('1.3.3', sha256='213e82bd716c9de6db2f98bcadbc4c24c7e2efe8c75939a1a84e28539c4e1748')
    version('1.3.2', sha256='91cfc3ed61dc40f47f050a109b08610667d73477af6ef36dcad31c31a4a8d53f')
    version('1.3.1', sha256='4773c0099dba767d963fd92143263be338c48702172e8754b9bc5103efe1c56c')
    version('1.3.0', sha256='fa2d64aac1f77e31dfbb270aeb08f5b32e27036a52ad15e69a77e309528010dc')

    depends_on('libvorbis')
    depends_on('id3lib')
