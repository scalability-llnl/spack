# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCnvkit(PythonPackage):
    """Copy number variation toolkit for high-throughput sequencing."""

    homepage = "https://github.com/etal/cnvkit"
    url      = "https://pypi.io/packages/source/C/CNVkit/CNVkit-0.9.6.tar.gz"

    version('0.9.6', sha256='be889c98a5cf0a994330b8c31c0a65151fb0095fe4e75a1e04118da2516248c2')

    depends_on('py-setuptools', type='build')
    depends_on('py-futures@3.0:', type=('build', 'run'), when='^python@:2.7')
    depends_on('py-biopython@1.62:', type=('build', 'run'))
    depends_on('py-future@0.15.2:', type=('build', 'run'))
    depends_on('py-pomegranate@0.9.0:', type=('build', 'run'))
    depends_on('py-matplotlib@1.3.1:', type=('build', 'run'))
    depends_on('py-numpy@1.9:', type=('build', 'run'))
    depends_on('py-pandas@0.20.1:0.24.999', type=('build', 'run'))
    depends_on('py-pyfaidx@0.4.7:', type=('build', 'run'))
    depends_on('py-pysam@0.10.0:', type=('build', 'run'))
    depends_on('py-reportlab@3.0:', type=('build', 'run'))
    depends_on('py-scipy@0.15.0:', type=('build', 'run'))
