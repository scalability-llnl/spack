# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lftp(AutotoolsPackage):
    """LFTP is a sophisticated file transfer program supporting a number
       of network protocols (ftp, http, sftp, fish, torrent)."""

    homepage = "http://lftp.yar.ru/"
    url      = "http://lftp.yar.ru/ftp/lftp-4.7.7.tar.gz"

    version('4.8.1', sha256='6117866215cd889dab30ff73292cd1d35fe0e12a9af5cd76d093500d07ab65a3')
    version('4.7.7', sha256='7bce216050094a1146ed05bed8fe5b3518224764ffe98884a848d44dc76fff8f')
    version('4.6.4', sha256='791e783779d3d6b519d0c23155430b9785f2854023eb834c716f5ba78873b15a')

    depends_on('expat')
    depends_on('iconv')
    depends_on('ncurses')
    depends_on('openssl')
    depends_on('readline')
    depends_on('zlib')

    def configure_args(self):
        return [
            '--with-expat={0}'.format(self.spec['expat'].prefix),
            '--with-libiconv={0}'.format(self.spec['iconv'].prefix),
            '--with-openssl={0}'.format(self.spec['openssl'].prefix),
            '--with-readline={0}'.format(self.spec['readline'].prefix),
            '--with-zlib={0}'.format(self.spec['zlib'].prefix),
            '--disable-dependency-tracking',
        ]
