# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTqdm(PythonPackage):
    """A Fast, Extensible Progress Meter"""

    homepage = "https://github.com/tqdm/tqdm"
    pypi = "tqdm/tqdm-4.45.0.tar.gz"

    version('4.59.0', sha256='d666ae29164da3e517fcf125e41d4fe96e5bb375cd87ff9763f6b38b5592fe33')
    version('4.45.0', sha256='00339634a22c10a7a22476ee946bbde2dbe48d042ded784e4d88e0236eca5d81')
    version('4.36.1', sha256='abc25d0ce2397d070ef07d8c7e706aede7920da163c64997585d42d3537ece3d')
    version('4.8.4',  sha256='bab05f8bb6efd2702ab6c532e5e6a758a66c0d2f443e09784b73e4066e6b3a37')

    variant('telegram', default=False, description='Enable Telegram bot support')
    variant('notebook', default=False, description='Enable Jupyter Notebook support')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools@42:', type=('build', 'run'))
    depends_on('py-setuptools-scm@3.4:+toml', type='build')
    depends_on('py-requests', when='+telegram', type=('build', 'run'))
    depends_on('py-ipywidgets@6:', when='+notebook', type=('build', 'run'))
