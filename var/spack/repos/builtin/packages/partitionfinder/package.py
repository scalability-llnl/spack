# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Partitionfinder(Package):
    """PartitionFinder is free open source software to select best-fit
       partitioning schemes and models of molecular evolution for
       phylogenetic analyses."""

    homepage = "https://github.com/brettc/partitionfinder"
    url      = "https://github.com/brettc/partitionfinder/archive/v2.1.1.tar.gz"

    version('2.1.1', sha256='ccf3718996ee6ca496909b4b97d2b075028e0543eba3bc47a8c14b689c84e061')

    depends_on('python@2.7.10:2.999', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-tables', type=('build', 'run'))
    depends_on('py-pyparsing', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree('partfinder', prefix.partfinder)
        install_tree('timings', prefix.timings)
        install('PartitionFinderMorphology.py', prefix.bin)
        install('PartitionFinderProtein.py', prefix.bin)
        install('PartitionFinder.py', prefix.bin)
