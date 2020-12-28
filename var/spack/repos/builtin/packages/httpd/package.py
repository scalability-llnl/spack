# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Httpd(AutotoolsPackage):
    """The Apache HTTP Server is a powerful and flexible HTTP/1.1 compliant
    web server."""

    homepage = "http://httpd.apache.org/"
    url      = "http://archive.apache.org/dist/httpd/httpd-2.4.43.tar.bz2"

    version('2.4.43', sha256='a497652ab3fc81318cdc2a203090a999150d86461acff97c1065dc910fe10f43')
    version('2.4.41', sha256='133d48298fe5315ae9366a0ec66282fa4040efa5d566174481077ade7d18ea40')
    version('2.4.39', sha256='b4ca9d05773aa59b54d66cd8f4744b945289f084d3be17d7981d1783a5decfa2')
    version('2.4.38', sha256='7dc65857a994c98370dc4334b260101a7a04be60e6e74a5c57a6dee1bc8f394a')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('apr')
    depends_on('apr-util')
    depends_on('pcre')

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--with-apr={0}'.format(spec['apr'].prefix),
            '--with-apr-util={0}'.format(spec['apr-util'].prefix)
        ]
        return config_args
