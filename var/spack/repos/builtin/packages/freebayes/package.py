# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Freebayes(MakefilePackage):
    """Bayesian haplotype-based genetic polymorphism discovery and
       genotyping."""

    homepage = "https://github.com/ekg/freebayes"
    git      = "https://github.com/ekg/freebayes.git"

    version('1.1.0', commit='39e5e4bcb801556141f2da36aba1df5c5c60701f',
            submodules=True)

    depends_on('cmake', type='build')
    depends_on('zlib')

    parallel = False

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        b = prefix.bin
        makefile.filter('cp bin/freebayes bin/bamleftalign /usr/local/bin/',
                        'cp bin/freebayes bin/bamleftalign {0}'.format(b))

    @run_before('install')
    def make_prefix_dot_bin(self):
        mkdir(prefix.bin)
