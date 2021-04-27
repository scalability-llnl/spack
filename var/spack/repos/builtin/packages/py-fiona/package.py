# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyFiona(PythonPackage):
    """Fiona reads and writes spatial data files."""

    homepage = "https://github.com/Toblerity/Fiona"
    pypi = "Fiona/Fiona-1.8.18.tar.gz"
    git      = "https://github.com/Toblerity/Fiona.git"

    maintainers = ['adamjstewart']

    version('master', branch='master')
    version('1.8.18', sha256='b732ece0ff8886a29c439723a3e1fc382718804bb057519d537a81308854967a')
    version('1.8.6',  sha256='fa31dfe8855b9cd0b128b47a4df558f1b8eda90d2181bff1dd9854e5556efb3e')
    version('1.7.12', sha256='8b54eb8422d7c502bb7776b184018186bede1a489cf438a7a47f992ade6a0e51')

    depends_on('python@3.6:', type=('build', 'link', 'run'), when='@1.9:')
    depends_on('python@2.6:', type=('build', 'link', 'run'))
    depends_on('gdal@1.11:', type=('build', 'link', 'run'), when='@1.9:')
    depends_on('gdal@1.8:', type=('build', 'link', 'run'))

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython', type='build', when='@master')
    depends_on('py-attrs@17:', type=('build', 'run'))
    depends_on('py-certifi', type=('build', 'run'), when='@1.8.18')
    depends_on('py-click@4:7', type=('build', 'run'))
    depends_on('py-cligj@0.5:', type=('build', 'run'))
    depends_on('py-click-plugins@1:', type=('build', 'run'))
    depends_on('py-six@1.7:', type=('build', 'run'))
    depends_on('py-munch', type=('build', 'run'))
    depends_on('py-argparse', type=('build', 'run'), when='^python@:2.6')
    depends_on('py-ordereddict', type=('build', 'run'), when='^python@:2.6')
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3')
