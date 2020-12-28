# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyTorchtext(PythonPackage):
    """Text utilities and datasets for PyTorch."""

    homepage = "https://github.com/pytorch/text"
    url      = "https://pypi.io/packages/source/t/torchtext/torchtext-0.5.0.tar.gz"

    maintainers = ['adamjstewart']

    version('0.5.0', sha256='7f22e24e9b939fff56b9118c78dc07aafec8dcc67164de15b9b5ed339e4179c6')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-tqdm', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-torch@0.4.0:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-sentencepiece', type=('build', 'run'))
