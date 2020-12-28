# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuast(PythonPackage):
    """Quality Assessment Tool for Genome Assemblies"""

    homepage = "http://cab.spbu.ru/software/quast"
    url      = "https://github.com/ablab/quast/archive/quast_4.6.1.tar.gz"

    version('4.6.3', sha256='d7f5e670563d17d683f6df057086f7b816b6a088266c6270f7114a1406aaab63')
    version('4.6.1', sha256='a8071188545710e5c0806eac612daaabde9f730819df2c44be3ffa9317b76a58')
    version('4.6.0', sha256='6bee86654b457a981718a19acacffca6a3e74f30997ad06162a70fd2a181ca2e')

    depends_on('boost@1.56.0')
    depends_on('perl@5.6.0:')
    depends_on('python@2.5:,3.3:')
    depends_on('py-setuptools',    type='build')
    depends_on('py-matplotlib',    type=('build', 'run'))
    depends_on('java',             type=('build', 'run'))
    depends_on('perl-time-hires',  type=('build', 'run'))
    depends_on('gnuplot',          type=('build', 'run'))
    depends_on('mummer',           type=('build', 'run'))
    depends_on('bedtools2',        type=('build', 'run'))
    depends_on('bwa',              type=('build', 'run'))
    depends_on('glimmer',          type=('build', 'run'))
