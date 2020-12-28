# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTornado(PythonPackage):
    """Tornado is a Python web framework and asynchronous networking
    library."""
    homepage = "https://github.com/tornadoweb/tornado"
    url      = "https://github.com/tornadoweb/tornado/archive/v6.0.3.tar.gz"

    version('6.0.3',   sha256='a97ac3b8c95867e534b48cb6fbbf156f5ca5b20c423bb06894c17b240d7a18fc')
    version('5.1.1', sha256='a1da335a2978b9a8c3544cab10076d799442d7988ed0b4f2be035fe4388ca8dd')
    version('4.4.0', sha256='ae556a0848e5d428d00597a18b38b9ca9d20f4600535e1dd33b3a576ab234194')

    depends_on('py-setuptools', type='build')

    # requirements from setup.py
    depends_on('python@3.5:', when='@6:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-backports-ssl-match-hostname', when='@:4 ^python@:2.7.8', type=('build', 'run'))
    depends_on('py-singledispatch', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-certifi', when='@:4 ^python@:3.3', type=('build', 'run'))
    depends_on('py-backports-abc@0.4:', when='^python@:3.4', type=('build', 'run'))
    depends_on('py-futures', when='@5: ^python@:3.1', type=('build', 'run'))
