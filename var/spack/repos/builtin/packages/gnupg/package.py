# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Gnupg(AutotoolsPackage):
    """GNU Pretty Good Privacy (PGP) package."""

    homepage = "https://gnupg.org/index.html"
    url      = "https://gnupg.org/ftp/gcrypt/gnupg/gnupg-2.2.19.tar.bz2"

    version('2.2.25', sha256='c55307b247af4b6f44d2916a25ffd1fb64ce2e509c3c3d028dbe7fbf309dc30a')
    version('2.2.24', sha256='9090b400faae34f08469d78000cfec1cee5b9c553ce11347cc96ef16eab98c46')
    version('2.2.23', sha256='10b55e49d78b3e49f1edb58d7541ecbdad92ddaeeb885b6f486ed23d1cd1da5c')
    version('2.2.22', sha256='7c1370565e1910b9d8c4e0fb57b9de34aa062ec7bb91abad5803d791f38d855b')
    version('2.2.21', sha256='61e83278fb5fa7336658a8b73ab26f379d41275bb1c7c6e694dd9f9a6e8e76ec')
    version('2.2.20', sha256='04a7c9d48b74c399168ee8270e548588ddbe52218c337703d7f06373d326ca30')
    version('2.2.19', sha256='242554c0e06f3a83c420b052f750b65ead711cc3fddddb5e7274fcdbb4e9dec0')
    version('2.2.17', sha256='afa262868e39b651a2db4c071fba90415154243e83a830ca00516f9a807fd514')
    version('2.2.15', sha256='cb8ce298d7b36558ffc48aec961b14c830ff1783eef7a623411188b5e0f5d454')
    version('2.2.3',  sha256='cbd37105d139f7aa74f92b6f65d136658682094b0e308666b820ae4b984084b4')
    version('2.1.21', sha256='7aead8a8ba75b69866f583b6c747d91414d523bfdfbe9a8e0fe026b16ba427dd')

    depends_on('npth@1.2:')
    depends_on('libgpg-error@1.24:')
    depends_on('libgcrypt@1.7.0:')
    depends_on('libksba@1.3.4:')
    depends_on('libassuan@2.4:', when='@:2.2.3')
    depends_on('libassuan@2.5:', when='@2.2.15:')
    depends_on('pinentry', type='run')
    depends_on('iconv')
    depends_on('zlib')

    def configure_args(self):
        args = [
            '--disable-bzip2',
            '--disable-sqlite',
            '--disable-ntbtls',
            '--disable-gnutls',
            '--disable-ldap',
            '--disable-regex',
            '--with-pinentry-pgm='        + self.spec['pinentry'].command.path,
            '--with-libgpg-error-prefix=' + self.spec['libgpg-error'].prefix,
            '--with-libgcrypt-prefix='    + self.spec['libgcrypt'].prefix,
            '--with-libassuan-prefix='    + self.spec['libassuan'].prefix,
            '--with-ksba-prefix='         + self.spec['libksba'].prefix,
            '--with-npth-prefix='         + self.spec['npth'].prefix,
            '--with-libiconv-prefix='     + self.spec['iconv'].prefix,
            '--with-zlib='                + self.spec['zlib'].prefix,
            '--without-tar',
            '--without-libiconv-prefix',
            '--without-readline',
        ]

        if self.run_tests:
            args.append('--enable-all-tests')

        return args
