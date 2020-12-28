# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nginx(AutotoolsPackage):
    """nginx [engine x] is an HTTP and reverse proxy server, a mail proxy
    server, and a generic TCP/UDP proxy server, originally written by Igor
    Sysoev."""

    homepage = "https://nginx.org/en/"
    url      = "https://nginx.org/download/nginx-1.12.0.tar.gz"

    version('1.15.6', sha256='a3d8c67c2035808c7c0d475fffe263db8c353b11521aa7ade468b780ed826cc6')
    version('1.13.8', sha256='8410b6c31ff59a763abf7e5a5316e7629f5a5033c95a3a0ebde727f9ec8464c5')
    version('1.12.0', sha256='b4222e26fdb620a8d3c3a3a8b955e08b713672e1bc5198d1e4f462308a795b30')

    depends_on('openssl')
    depends_on('pcre')
    depends_on('zlib')

    conflicts('%gcc@8:', when='@:1.14')

    def configure_args(self):
        args = ['--with-http_ssl_module']
        return args

    def setup_run_environment(self, env):
        """Prepend the sbin directory to PATH."""
        env.prepend_path('PATH', self.prefix.sbin)
