# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyGpytorch(PythonPackage):
    """GPyTorch is a Gaussian process library implemented using PyTorch.
    GPyTorch is designed for creating scalable, flexible, and modular Gaussian
    process models with ease."""

    homepage = "https://gpytorch.ai/"
    url      = "https://pypi.io/packages/source/g/gpytorch/gpytorch-1.2.1.tar.gz"

    maintainers = ['adamjstewart']

    version('1.2.1', sha256='ddd746529863d5419872610af23b1a1b0e8a29742131c9d9d2b4f9cae3c90781')
    version('1.2.0', sha256='fcb216e0c1f128a41c91065766508e91e487d6ffadf212a51677d8014aefca84')
    version('1.1.1', sha256='76bd455db2f17af5425f73acfaa6d61b8adb1f07ad4881c0fa22673f84fb571a')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-torch@1.6:', when='@1.2:', type=('build', 'run'))
    depends_on('py-torch@1.5:', type=('build', 'run'))
    depends_on('py-scikit-learn', when='@1.2:', type=('build', 'run'))
    depends_on('py-scipy', when='@1.2:', type=('build', 'run'))
