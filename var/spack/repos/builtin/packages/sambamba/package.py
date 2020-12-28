# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sambamba(Package):
    """Sambamba: process your BAM data faster (bioinformatics)"""

    homepage = "http://lomereiter.github.io/sambamba/"
    git      = "https://github.com/lomereiter/sambamba.git"

    version('0.6.6', tag='v0.6.6', submodules=True)

    depends_on('ldc~shared', type=('build', 'link'))
    depends_on('python', type='build')

    resource(
        name='undeaD',
        git='https://github.com/dlang/undeaD.git',
        tag='v1.0.7',
    )

    patch('Makefile.patch')
    parallel = False

    def install(self, spec, prefix):
        make('sambamba-ldmd2-64')
        mkdirp(prefix.bin)
        for filename in ('build/sambamba', 'build/sambamba.debug'):
            install(filename, prefix.bin)
