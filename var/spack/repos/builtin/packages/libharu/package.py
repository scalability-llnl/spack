# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Libharu(AutotoolsPackage):
    """libharu - free PDF library.

    Haru is a free, cross platform, open-sourced software library for
    generating PDF."""

    homepage = "http://libharu.org"
    url      = "https://github.com/libharu/libharu/archive/RELEASE_2_3_0.tar.gz"
    git      = "https://github.com/libharu/libharu.git"

    version('master', branch='master')
    version('2.3.0', sha256='8f9e68cc5d5f7d53d1bc61a1ed876add1faf4f91070dbc360d8b259f46d9a4d2')
    version('2.2.0', sha256='5e63246d2da0272a9dbe5963fd827c7efa6e29d97a2d047c0d4c5f0b780f10b5')

    depends_on('libtool', type=('build'))
    depends_on('autoconf', type=('build'))
    depends_on('automake', type=('build'))
    depends_on('libpng')
    depends_on('zlib')

    def autoreconf(self, spec, prefix):
        """execute their autotools wrapper script"""
        if os.path.exists('./buildconf.sh'):
            bash = which('bash')
            bash('./buildconf.sh', '--force')

    def configure_args(self):
        """Point to spack-installed zlib and libpng"""
        spec = self.spec
        args = []

        args.append('--with-zlib={0}'.format(spec['zlib'].prefix))
        args.append('--with-png={0}'.format(spec['libpng'].prefix))

        return args

    def url_for_version(self, version):
        url = 'https://github.com/libharu/libharu/archive/RELEASE_{0}.tar.gz'
        return url.format(version.underscored)
