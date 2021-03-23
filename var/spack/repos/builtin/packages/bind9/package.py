# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bind9(AutotoolsPackage):
    """
    BIND 9 has evolved to be a very flexible, full-featured DNS system.
    """

    homepage = "https://github.com/isc-projects/bind9"
    url      = "https://github.com/isc-projects/bind9/archive/v9_14_6.tar.gz"

    version('9_14_6', sha256='98be7a7b6d614b519f6c8d6ec7a8a39759ae9604d87228d9dc7c034471e5433e')

    depends_on('libuv', type='link')
    depends_on('pkgconfig', type='build')
    depends_on('openssl', type='link')
    depends_on('libiconv', type='link')

    def configure_args(self):
        args = ["--without-python", "--disable-linux-caps",
                '--with-openssl={0}'.format(self.spec['openssl'].prefix)]
        return args
