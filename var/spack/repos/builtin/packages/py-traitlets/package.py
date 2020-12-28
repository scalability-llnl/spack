# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTraitlets(PythonPackage):
    """Traitlets Python config system"""

    homepage = "https://pypi.python.org/pypi/traitlets"
    url      = "https://pypi.io/packages/source/t/traitlets/traitlets-5.0.4.tar.gz"

    version('5.0.4', sha256='86c9351f94f95de9db8a04ad8e892da299a088a64fd283f9f6f18770ae5eae1b')
    version('4.3.3', sha256='d023ee369ddd2763310e4c3eae1ff649689440d4ae59d7485eb4cfbbe3e359f7')
    version('4.3.2', sha256='9c4bd2d267b7153df9152698efb1050a5d84982d3384a37b2c1f7723ba3e7835')
    version('4.3.1', sha256='ba8c94323ccbe8fd792e45d8efe8c95d3e0744cc8c085295b607552ab573724c')
    version('4.3.0', sha256='8a33cb7b1ef47f2d6dc16e9cf971217d5a4882a3541c070e78a0e8e8edcb3f82')
    version('4.2.2', sha256='7d7e3070484b2fe490fa55e0acf7023afc5ed9ddabec57405f25c355158e152a')
    version('4.2.1', sha256='76eba33c89723b8fc024f950cacaf5bf2ef37999642cc9a61f4e7c1ca5cf0ac0')
    version('4.2.0', sha256='e4c39210f2f2ff7361b86043b6512adbcf6f024b44b501f7b42fd9a23402dea9')
    version('4.1.0', sha256='440e38dfa5d2a26c086d4b427cfb7aed17d0a2dca78bce90c33354da2592af5b')
    version('4.0.0', sha256='0b140b4a94a4f1951887d9bce4650da211f79600fc9fdb422acc90c5bbe0233b')

    depends_on('python@3.7:', when='@5:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-six', when='@:4', type=('build', 'run'))
    depends_on('py-decorator', when='@:4', type=('build', 'run'))
    depends_on('py-enum34', when='^python@:3.3', type=('build', 'run'))
