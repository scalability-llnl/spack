# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmicrohttpd(AutotoolsPackage):
    """GNU libmicrohttpd is a small C library that is supposed to make
       it easy to run an HTTP server as part of another application.
    """

    homepage = "https://www.gnu.org/software/libmicrohttpd/"
    url      = "https://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-0.9.71.tar.gz"

    maintainers = ['hainest']

    version('0.9.71', 'e8f445e85faf727b89e9f9590daea4473ae00ead38b237cf1eda55172b89b182')
    version('0.9.70', '90d0a3d396f96f9bc41eb0f7e8187796049285fabef82604acd4879590977307')

    variant('https',
            default=False,
            description="HTTPS support with GnuTLS")

    depends_on('gettext')
    depends_on('gnutls', when='+https')
    depends_on('libgcrypt', when='+https')

    def configure_args(self):
        options = [
            '--enable-static=no',   # don't build static libs
            '--enable-shared=yes',  # always build shared libs
            '--with-pic',           # always build PIC libs
            '--disable-rpath',      # let spack handle the RPATH
            '--disable-doc',        # don't build the docs
            '--disable-examples',   # don't build the examples
            '--disable-curl'		# disable cURL-based testcases
        ]

        if self.spec.satisfies('+https'):
            options.append('--enable-https')
            prefix = self.spec['gnutls'].prefix
            options.append('--with-gnutls={0}'.format(prefix))
            prefix = self.spec['libgcrypt'].prefix
            options.append('--with-libgcrypt-prefix={0}'.format(prefix))

        return options
