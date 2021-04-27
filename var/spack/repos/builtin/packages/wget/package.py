# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wget(AutotoolsPackage, GNUMirrorPackage):
    """GNU Wget is a free software package for retrieving files using
    HTTP, HTTPS and FTP, the most widely-used Internet protocols. It is a
    non-interactive commandline tool, so it may easily be called from scripts,
    cron jobs, terminals without X-Windows support, etc."""

    homepage = "http://www.gnu.org/software/wget/"
    gnu_mirror_path = "wget/wget-1.19.1.tar.gz"

    version('1.21',   sha256='b3bc1a9bd0c19836c9709c318d41c19c11215a07514f49f89b40b9d50ab49325')
    version('1.20.3', sha256='31cccfc6630528db1c8e3a06f6decf2a370060b982841cfab2b8677400a5092e')
    version('1.19.1', sha256='9e4f12da38cc6167d0752d934abe27c7b1599a9af294e73829be7ac7b5b4da40')
    version('1.17',   sha256='3e04ad027c5b6ebd67c616eec13e66fbedb3d4d8cbe19cc29dadde44b92bda55')
    version('1.16',   sha256='b977fc10ac7a72d987d48136251aeb332f2dced1aabd50d6d56bdf72e2b79101')

    variant('ssl', default='openssl', values=('gnutls', 'openssl'),
            description='Specify SSL backend')
    variant('zlib', default=True,
            description='Enable zlib support')
    variant('libpsl', default=False,
            description='Enable support for libpsl cookie checking')
    variant('pcre', default=False,
            description='Enable PCRE style regular expressions')
    variant('python', default=False,
            description='Enable Python support')

    depends_on('gnutls',  when='ssl=gnutls')
    depends_on('openssl', when='ssl=openssl')

    depends_on('gettext', type='build')
    depends_on('python@3:', type='build', when='+python')

    depends_on('zlib', when='+zlib')
    depends_on('libpsl', when='+libpsl')
    depends_on('pcre', when='+pcre')

    depends_on('perl@5.12.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('iconv')

    depends_on('valgrind', type='test')

    build_directory = 'spack-build'

    def configure_args(self):
        spec = self.spec

        args = [
            '--with-ssl={0}'.format(spec.variants['ssl'].value),
        ]

        if '+zlib' in spec:
            args.append('--with-zlib')
        else:
            args.append('--without-zlib')

        if '+libpsl' in spec:
            args.append('--with-libpsl')
        else:
            args.append('--without-libpsl')

        if '+pcre' in spec:
            args.append('--enable-pcre')
        else:
            args.append('--disable-pcre')

        if self.run_tests:
            args.append('--enable-valgrind-tests')
        else:
            args.append('--disable-valgrind-tests')

        return args
