# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pcre(AutotoolsPackage):
    """The PCRE package contains Perl Compatible Regular Expression
    libraries. These are useful for implementing regular expression
    pattern matching using the same syntax and semantics as Perl 5."""

    homepage = "http://www.pcre.org"
    url      = "https://ftp.pcre.org/pub/pcre/pcre-8.42.tar.bz2"

    version('8.44', sha256='19108658b23b3ec5058edc9f66ac545ea19f9537234be1ec62b714c84399366d')
    version('8.43', sha256='91e762520003013834ac1adb4a938d53b22a216341c061b0cf05603b290faf6b')
    version('8.42', sha256='2cd04b7c887808be030254e8d77de11d3fe9d4505c39d4b15d2664ffe8bf9301')
    version('8.41', sha256='e62c7eac5ae7c0e7286db61ff82912e1c0b7a0c13706616e94a7dd729321b530')
    version('8.40', sha256='00e27a29ead4267e3de8111fcaa59b132d0533cdfdbdddf4b0604279acbcf4f4')
    version('8.39', sha256='b858099f82483031ee02092711689e7245586ada49e534a06e678b8ea9549e8b')
    version('8.38', sha256='b9e02d36e23024d6c02a2e5b25204b3a4fa6ade43e0a5f869f254f49535079df')

    patch('intel.patch', when='@8.38')

    variant('jit', default=False,
            description='Enable JIT support.')

    variant('multibyte', default=True,
            description='Enable support for 16 and 32 bit characters.')

    variant('utf', default=True,
            description='Enable support for UTF-8/16/32, '
            'incompatible with EBCDIC.')

    def configure_args(self):
        args = []

        if '+jit' in self.spec:
            args.append('--enable-jit')

        if '+multibyte' in self.spec:
            args.append('--enable-pcre16')
            args.append('--enable-pcre32')

        if '+utf' in self.spec:
            args.append('--enable-utf')
            args.append('--enable-unicode-properties')

        return args
