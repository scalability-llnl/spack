# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMccabe(PythonPackage):
    """Ned's script to check McCabe complexity."""

    homepage = "https://github.com/PyCQA/mccabe"
    url      = "https://github.com/PyCQA/mccabe/archive/0.5.2.tar.gz"

    version('0.6.1', sha256='2748af6516175b94be318cd8226fa50b5339b9dc886bce378ac2afb37a157524')
    version('0.6.0', sha256='f42593f451106965053fa852dfd395b85a2fcb6df960e268cb7a1d60d4aec291')
    version('0.5.3', sha256='4a1582dfe070e630387710169e4731a1b0a4eab736431fa25e91f1fcaf3cbe94')
    version('0.5.2', sha256='a456c9e2529bf4e7e9e690b20557c5ae5d9cbe25df2a0bbc73dcc39b1b959f4b')
    version('0.5.1', sha256='31377e7d65ac6458b1f788bf50c34f788f173334383cbfeadd701f772a0f3fe1')
    version('0.5.0', sha256='b10a4de7987f0e4d6be2a073d1bc91ceed5f0a3715c6088520253e2452ea5dfe')
    version('0.4.0', sha256='1c0b443fb11dbf90e7caff4366299c0fd69d6bb0c6fedb46fa74283628d8d3ff')
    version('0.3.1', sha256='244134b78607b74d885ba45f29e495e55c75a261b02de62976233d47e64949ea')
    version('0.3',   sha256='8ef89519a7ce6036597a6bd4d0f28a921cb949cba1bbe42570e5255c6f31456b')
    version('0.2.1', sha256='88506c11597a4258719b1c7e72317b2145cb43da63314b05d11cd5433dd5a813')
    version('0.2',   sha256='3cc0ff234082035ef4f73640d96ca3f52d6e2e9865a38181093e836370b5f7c3')
    version('0.1',   sha256='10023fc9a64ea25b6cde1f6d0b824990a9882c9086a54b2bcfb8aa70d5ca179f')

    depends_on('python@2.7:2.8,3.3:')

    depends_on('py-setuptools', type='build')

    def patch(self):
        """Filter pytest-runner requirement out of setup.py."""
        filter_file("['pytest-runner']", "[]", 'setup.py', string=True)
