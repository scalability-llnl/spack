# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libiconv(AutotoolsPackage, GNUMirrorPackage):
    """GNU libiconv provides an implementation of the iconv() function
    and the iconv program for character set conversion."""

    homepage = "https://www.gnu.org/software/libiconv/"
    gnu_mirror_path = "libiconv/libiconv-1.16.tar.gz"

    version('1.16', sha256='e6a1b1b589654277ee790cce3734f07876ac4ccfaecbee8afa0b649cf529cc04')
    version('1.15', sha256='ccf536620a45458d26ba83887a983b96827001e92a13847b45e4925cc8913178')
    version('1.14', sha256='72b24ded17d687193c3366d0ebe7cde1e6b18f0df8c55438ac95be39e8a30613')

    # We cannot set up a warning for gets(), since gets() is not part
    # of C11 any more and thus might not exist.
    patch('gets.patch', when='@1.14')
    provides('iconv')

    conflicts('@1.14', when='%gcc@5:')

    def configure_args(self):
        args = ['--enable-extra-encodings']

        # A hack to patch config.guess in the libcharset sub directory
        copy('./build-aux/config.guess',
             'libcharset/build-aux/config.guess')
        return args
