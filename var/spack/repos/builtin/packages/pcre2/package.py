# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pcre2(AutotoolsPackage):
    """The PCRE2 package contains Perl Compatible Regular Expression
       libraries. These are useful for implementing regular expression
       pattern matching using the same syntax and semantics as Perl 5."""

    homepage = "http://www.pcre.org"
    url      = "https://ftp.pcre.org/pub/pcre/pcre2-10.31.tar.bz2"

    version('10.36', sha256='a9ef39278113542968c7c73a31cfcb81aca1faa64690f400b907e8ab6b4a665c')
    version('10.35', sha256='9ccba8e02b0ce78046cdfb52e5c177f0f445e421059e43becca4359c669d4613')
    version('10.31', sha256='e07d538704aa65e477b6a392b32ff9fc5edf75ab9a40ddfc876186c4ff4d68ac')
    version('10.20', sha256='332e287101c9e9567d1ed55391b338b32f1f72c5b5ee7cc81ef2274a53ad487a')

    variant('multibyte', default=True,
            description='Enable support for 16 and 32 bit characters.')
    variant('jit', default=False,
            description='enable Just-In-Time compiling support')

    def configure_args(self):
        args = []

        if '+multibyte' in self.spec:
            args.append('--enable-pcre2-16')
            args.append('--enable-pcre2-32')

        if '+jit' in self.spec:
            args.append('--enable-jit')

        return args

    @property
    def libs(self):
        if '+multibyte' in self.spec:
            name = 'libpcre2-32'
        else:
            name = 'libpcre2-8'

        return find_libraries(name, root=self.prefix, recursive=True)
