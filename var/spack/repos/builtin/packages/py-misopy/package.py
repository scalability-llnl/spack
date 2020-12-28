# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMisopy(PythonPackage):
    """MISO (Mixture of Isoforms) is a probabilistic framework that
       quantitates the expression level of alternatively spliced genes from
       RNA-Seq data, and identifies differentially regulated isoforms or exons
       across samples."""

    homepage = "http://miso.readthedocs.io/en/fastmiso/"
    url      = "https://pypi.io/packages/source/m/misopy/misopy-0.5.4.tar.gz"

    version('0.5.4', sha256='377a28b0c254b1920ffdc2d89cf96c3a21cadf1cf148ee6d6ef7a88ada067dfc')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-numpy@1.5.0:', type=('build', 'run'))
    depends_on('py-scipy@0.9.0:', type=('build', 'run'))
    depends_on('py-pysam@0.6.0:', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('samtools')
    depends_on('bedtools2')
