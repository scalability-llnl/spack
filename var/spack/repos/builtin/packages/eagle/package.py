# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Eagle(MakefilePackage):
    """EAGLE: Explicit Alternative Genome Likelihood Evaluator"""

    homepage = "https://github.com/tony-kuo/eagle"
    url      = "https://github.com/tony-kuo/eagle/archive/v1.1.2.tar.gz"

    version('1.1.2', sha256='afe967560d1f8fdbd0caf4b93b5f2a86830e9e4d399fee4a526140431343045e')

    depends_on('curl')
    depends_on('zlib')
    depends_on('lzma')
    depends_on('htslib')

    def edit(self, spec, prefix):
        # remove unused gcc flags
        filter_file('$(LFLAGS) $(INCLUDES)', '', 'Makefile', string=True)

        # drop static link to htslib
        filter_file('$(LIBS)', '', 'Makefile', string=True)

        # don't try to build htslib.
        filter_file('all: UTIL HTSLIB', 'all: UTIL',
                    'Makefile', string=True)

        # add htslib link to ldflags
        filter_file('-lcurl', '-lcurl -lhts', 'Makefile', string=True)

        # use spack C compiler
        filter_file('CC=.*', 'CC={0}'.format(spack_cc), 'Makefile')

        # remove march=native %fj
        if self.spec.satisfies('%fj'):
            filter_file('-march=native', '', 'Makefile', string=True)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        bins = [
            'eagle',
            'eagle-rc',
            'eagle-nm',
        ]

        for b in bins:
            install(b, prefix.bin)
