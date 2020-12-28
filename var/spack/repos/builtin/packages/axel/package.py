# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Axel(AutotoolsPackage):
    """Axel is a light command line download accelerator for Linux and Unix"""

    homepage = "https://github.com/axel-download-accelerator/axel"
    url      = "https://github.com/axel-download-accelerator/axel/archive/v2.16.1.tar.gz"

    version('2.16.1', sha256='64529add74df3db828f704b42d4ec3fcdacb8142c84f051f9213637c337e706c')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('gettext')
    depends_on('openssl')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')
