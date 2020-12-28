# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bucky(MakefilePackage):
    """BUCKy is a free program to combine molecular data from multiple loci.
       BUCKy estimates the dominant history of sampled individuals, and how
       much of the genome supports each relationship, using Bayesian
       concordance analysis."""

    homepage = "http://www.stat.wisc.edu/~ane/bucky/index.html"
    url      = "http://dstats.net/download/http://www.stat.wisc.edu/~ane/bucky/v1.4/bucky-1.4.4.tgz"

    version('1.4.4', sha256='1621fee0d42314d9aa45d0082b358d4531e7d1d1a0089c807c1b21fbdc4e4592')

    # Compilation requires gcc
    conflicts('%cce')
    conflicts('%apple-clang')
    conflicts('%clang')
    conflicts('%intel')
    conflicts('%nag')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')

    build_directory = 'src'

    def install(self, spec, prefix):
        with working_dir('src'):
            mkdirp(prefix.bin)
            install('bucky', prefix.bin)
            install('mbsum', prefix.bin)
        install_tree('data', prefix.data)
        install_tree('doc', prefix.doc)
        install_tree('scripts', prefix.scripts)
