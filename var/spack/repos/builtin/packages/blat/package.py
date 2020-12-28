# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Blat(Package):
    """BLAT (BLAST-like alignment tool) is a pairwise sequence
       alignment algorithm."""

    homepage = "https://genome.ucsc.edu/FAQ/FAQblat.html"
    url      = "https://users.soe.ucsc.edu/~kent/src/blatSrc35.zip"

    version('35', sha256='06d9bcf114ec4a4b21fef0540a0532556b6602322a5a2b33f159dc939ae53620')

    depends_on('libpng')

    def setup_build_environment(self, env):
        env.set('MACHTYPE', 'x86_64')

    def install(self, spec, prefix):
        filter_file('CC=.*', 'CC={0}'.format(spack_cc), 'inc/common.mk')
        mkdirp(prefix.bin)
        make("BINDIR=%s" % prefix.bin)
