# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Libtheora(AutotoolsPackage):
    """Theora Video Compression."""

    homepage = "http://www.theora.org"
    url      = "http://downloads.xiph.org/releases/theora/libtheora-1.1.1.tar.xz"

    version('1.1.1',       sha256='f36da409947aa2b3dcc6af0a8c2e3144bc19db2ed547d64e9171c59c66561c61')
    version('1.1.0',       sha256='3d7b4fb1c115f1a530afd430eed2e8861fa57c8b179ec2d5a5d8f1cd0c7a4268')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('doxygen',  type='build')
    depends_on('libogg')
    depends_on('libpng')

    patch('exit-prior-to-running-configure.patch', when='@1.1.1')
    patch('fix_encoding.patch', when='@1.1:')
    patch('https://gitlab.xiph.org/xiph/theora/-/commit/7288b539c52e99168488dc3a343845c9365617c8.patch',
          sha256='2e4f891f6880386d9391f3e4eaf4a23493de4eea532f9b5cb8a04b5f7cd09301', when='^libpng@1.6:')

    def autoreconf(self, spec, prefix):
        sh = which('sh')
        if self.spec.satisfies('target=aarch64:'):
            sh('./autogen.sh', 'prefix={0}'.format(prefix),
               '--build=arm-linux')
        else:
            sh('./autogen.sh', 'prefix={0}'.format(prefix))
