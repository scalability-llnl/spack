# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pigz(MakefilePackage):
    """A parallel implementation of gzip for modern multi-processor,
       multi-core machines."""

    homepage = "http://zlib.net/pigz/"
    url      = "https://github.com/madler/pigz/archive/v2.3.4.tar.gz"

    version('2.4', sha256='e228e7d18b34c4ece8d596eb6eee97bde533c6beedbb728d07d3abe90b4b1b52')
    version('2.3.4', sha256='763f2fdb203aa0b7b640e63385e38e5dd4e5aaa041bc8e42aa96f2ef156b06e8')

    depends_on('zlib')

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man1)
        install('pigz', "%s/pigz" % prefix.bin)
        install('pigz.1', "%s/pigz.1" % prefix.man.man1)
