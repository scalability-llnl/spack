# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPicrust(PythonPackage):
    """bioinformatics software package designed to predict metagenome
        functional content from marker gene surveys and full genomes."""

    homepage = "http://picrust.github.io/picrust/index.html"
    url      = "https://github.com/picrust/picrust/releases/download/v1.1.3/picrust-1.1.3.tar.gz"

    version('1.1.3', sha256='7538c8544899b8855deb73a2d7a4ccac4808ff294e161530a8c8762d472d8906')

    depends_on('python@2.7:2.999', type=('build', 'run'))
    depends_on('py-cogent@1.5.3', type=('build', 'run'))
    depends_on('py-biom-format@2.1.4:2.1.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-future@0.16.0', type=('build', 'run'))
    depends_on('py-numpy@1.5.1:', type=('build', 'run'))
