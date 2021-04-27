# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImportlibMetadata(PythonPackage):
    """Read metadata from Python packages."""

    homepage = "https://importlib-metadata.readthedocs.io/"
    pypi = "importlib_metadata/importlib_metadata-1.2.0.tar.gz"

    version('3.10.0', sha256='c9db46394197244adf2f0b08ec5bc3cf16757e9590b02af1fca085c16c0d600a')
    version('2.0.0', sha256='77a540690e24b0305878c37ffd421785a6f7e53c8b5720d211b211de8d0e95da')
    version('1.2.0', sha256='41e688146d000891f32b1669e8573c57e39e5060e7f5f647aa617cd9a9568278')
    version('0.23',  sha256='aa18d7378b00b40847790e7c27e11673d7fed219354109d0e7b9e5b25dc3ad26')
    version('0.19',  sha256='23d3d873e008a513952355379d93cbcab874c58f4f034ff657c7a87422fa64e8')
    version('0.18',  sha256='cb6ee23b46173539939964df59d3d72c3e0c1b5d54b84f1d8a7e912fe43612db')

    depends_on('python@3.6:', type=('build', 'run'), when='@3:')
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-setuptools-scm@3.4.1:+toml', type='build', when='@3:')
    depends_on('py-zipp@0.5:', type=('build', 'run'))
    depends_on('py-pathlib2', when='^python@:2', type=('build', 'run'))
    depends_on('py-contextlib2', when='^python@:2', type=('build', 'run'))
    depends_on('py-configparser@3.5:', when='^python@:2', type=('build', 'run'))
    depends_on('py-typing-extensions@3.6.4:', type=('build', 'run'), when='@3: ^python@:3.7.999')
