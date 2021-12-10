# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHist(PythonPackage):
    """Hist classes and utilities"""

    homepage = "https://github.com/scikit-hep/hist"
    pypi     = "hist/hist-2.5.2.tar.gz"

    version('2.5.2', sha256='0bafb8b956cc041f1b26e8f5663fb8d3b8f7673f56336facb84d8cfdc30ae2cf')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-boost-histogram@1.2.0:1.2', type=('build', 'run'))
    depends_on('py-histoprint@2.2.0:', type=('build', 'run'))
    depends_on('py-numpy@1.14.5:', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7:', type=('build', 'run'), when='^python@:3.7')
    depends_on('py-mplhep', type=('build', 'run'))
