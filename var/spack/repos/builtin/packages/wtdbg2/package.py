# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wtdbg2(MakefilePackage):
    """A fuzzy Bruijn graph approach to long noisy reads assembly"""

    homepage = "https://github.com/ruanjue/wtdbg2"
    url      = "https://github.com/ruanjue/wtdbg2/archive/v2.3.tar.gz"

    version('2.3', sha256='fb61d38a4c60a39b3b194e63b855141c05ddcbe71cf244ae613766a9b0a56621')

    depends_on('zlib')

    def install(self, spec, prefix):
        make('install', 'BIN=%s' % prefix.bin)
