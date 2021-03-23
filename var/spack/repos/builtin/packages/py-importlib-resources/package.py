# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImportlibResources(PythonPackage):
    """Read resources from Python packages"""

    pypi = "importlib_resources/importlib_resources-1.0.2.tar.gz"

    version('5.1.0', sha256='bfdad047bce441405a49cf8eb48ddce5e56c696e185f59147a8b79e75e9e6380')
    version('1.0.2', sha256='d3279fd0f6f847cced9f7acc19bd3e5df54d34f93a2e7bb5f238f81545787078')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    depends_on('python@3.6:', when='@5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@3.4.1:+toml', when='@5:', type='build')
    depends_on('py-zipp@0.4:', when='@5:', type=('build', 'run'))
    depends_on('py-wheel', when='@1.0.2', type='build')
    depends_on('py-pathlib2', when='^python@:2', type=('build', 'run'))
    depends_on('py-typing', when='^python@:3.4', type=('build', 'run'))
