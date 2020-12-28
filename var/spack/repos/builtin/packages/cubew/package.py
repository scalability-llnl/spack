# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cubew(AutotoolsPackage):
    """Component of CubeBundle: High performance C Writer library """

    homepage = "http://www.scalasca.org/software/cube-4.x/download.html"
    url = "http://apps.fz-juelich.de/scalasca/releases/cube/4.4/dist/cubew-4.4.tar.gz"

    version('4.5', sha256='16bd8fd864197a74ca65f7325761ad75d73d555072326e95e1338cff39f28a5c')
    version('4.4.3', sha256='93fff6cc1e8b0780f0171ef5302a2e1a257f99b6383fbfc1b9b82f925ceff501')
    version('4.4.2', sha256='31a71e9a05e6523de2b86b4026821bbb75fb411eb5b18ae38b27c1f44158014a')
    version('4.4.1', sha256='c09e3f5a3533ebedee2cc7dfaacd7bac4680c14c3fa540669466583a23f04b67')
    version('4.4',   sha256='b1d6fecb546bc645ced430ea3fc166e85835f3b997d4e5f0dece71919fc95a99')

    depends_on('pkgconfig', type='build')
    depends_on('zlib')

    def url_for_version(self, version):
        url = 'http://apps.fz-juelich.de/scalasca/releases/cube/{0}/dist/cubew-{1}.tar.gz'

        return url.format(version.up_to(2), version)

    def configure_args(self):
        configure_args = ['--enable-shared']

        return configure_args

    def install(self, spec, prefix):
        make('install', parallel=True)
