# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rsem(MakefilePackage):
    """RSEM is a software package for estimating gene and isoform expression
       levels from RNA-Seq data."""

    homepage = "http://deweylab.github.io/RSEM/"
    url      = "https://github.com/deweylab/RSEM/archive/v1.3.0.tar.gz"

    version('1.3.1', sha256='93c749a03ac16e94b1aab94d032d4fd5687d3261316ce943ecb89d3ae3ec2e11')
    version('1.3.0', sha256='ecfbb79c23973e1c4134f05201f4bd89b0caf0ce4ae1ffd7c4ddc329ed4e05d2')

    depends_on('r', type=('build', 'run'))
    depends_on('perl', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
    depends_on('bowtie')
    depends_on('bowtie2')
    depends_on('star')

    def install(self, spec, prefix):
        make('install', 'DESTDIR=%s' % prefix, 'prefix=')
