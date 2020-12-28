# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HicPro(MakefilePackage):
    """HiC-Pro is a package designed to process Hi-C data,
    from raw fastq files (paired-end Illumina data)
    to the normalized contact maps"""

    homepage = "https://github.com/nservant/HiC-Pro"
    url      = "https://github.com/nservant/HiC-Pro/archive/v2.10.0.tar.gz"

    version('2.10.0', sha256='df181ea5c57247caf6b25fd15dfbb03df597ff8c4f57599d88607648bb61f1b7')

    depends_on('bowtie2')
    depends_on('samtools')
    depends_on('python+ucs4@2.7:2.8')
    depends_on('r')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))
    depends_on('py-bx-python', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))

    def edit(self, spec, prefix):
        config = FileFilter('config-install.txt')
        config.filter('PREFIX =.*', 'PREFIX = {0}'.format(prefix))
        config.filter('BOWTIE2 PATH =.*',
                      'BOWTIE2_PATH = {0}'.format(spec['bowtie2'].prefix))
        config.filter('SAMTOOLS_PATH =.*',
                      'SAMTOOLS_PATH = {0}'.format(spec['samtools'].prefix))
        config.filter('R_PATH =.*',
                      'R_RPTH ={0}'.format(spec['r'].prefix))
        config.filter('PYTHON_PATH =.*',
                      'PYTHON_RPTH ={0}'.format(spec['python'].prefix))

    def build(self, spec, preifx):
        make('-f', './scripts/install/Makefile',
             'CONFIG_SYS=./config-install.txt')
        make('mapbuilder')
        make('readstrimming')
        make('iced')

    def install(self, spec, prefix):
        # Patch INSTALLPATH in config-system.txt
        config = FileFilter('config-system.txt')
        config.filter('/HiC-Pro_%s' % self.version, '')
        # Install
        install('config-hicpro.txt', prefix)
        install('config-install.txt', prefix)
        install('config-system.txt', prefix)
        install_tree('bin', prefix.bin)
        install_tree('annotation', prefix.annotation)
        install_tree('doc', prefix.doc)
        install_tree('scripts', prefix.scripts)
        install_tree('test-op', join_path(prefix, 'test-op'))
