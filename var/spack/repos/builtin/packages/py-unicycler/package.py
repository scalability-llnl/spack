# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUnicycler(PythonPackage):
    """Unicycler is an assembly pipeline for bacterial genomes. It can
    assemble Illumina-only read sets where it functions as a SPAdes-optimiser.
    It can also assembly long-read-only sets (PacBio or Nanopore) where it
    runs a miniasm+Racon pipeline. For the best possible assemblies, give it
    both Illumina reads and long reads, and it will conduct a hybrid assembly.
    """

    homepage = "https://github.com/rrwick/Unicycler"
    url      = "https://github.com/rrwick/Unicycler/archive/v0.4.5.tar.gz"

    version('0.4.7', sha256='a8cf65e46dc2694b0fbd4e9190c73a1f300921457aadfab27a1792b785620d63')
    version('0.4.6', sha256='56f6f358a5d1f8dd0fcd1df04504079fc42cec8453a36ee59ff89295535d03f5')
    version('0.4.5', sha256='67043656b31a4809f8fa8f73368580ba7658c8440b9f6d042c7f70b5eb6b19ae')

    depends_on('python@3.4:', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('spades', type='run')
    depends_on('pilon', type='run')
    depends_on('jdk', type=('build', 'run'))
    depends_on('bowtie2', type='run')
    depends_on('samtools@1.0:', type=('build', 'link', 'run'))
    depends_on('racon', type=('build', 'link', 'run'))
    depends_on('blast-plus', type='run')

    conflicts('%gcc@:4.9.0')
    conflicts('%clang@:3.4.2')
