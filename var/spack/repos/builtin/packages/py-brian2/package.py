# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBrian2(PythonPackage):
    """A clock-driven simulator for spiking neural networks"""

    homepage = "http://www.briansimulator.org"
    url      = "https://pypi.io/packages/source/B/Brian2/Brian2-2.2.2.1.tar.gz"

    version('2.2.2.1', sha256='02075f66d42fd243fc5e28e1add8862709ae9fdabaffb69858e6d7f684a91525')
    version('2.0.1',   sha256='195d8ced0d20e9069917776948f92aa70b7457bbc6b5222b8199654402ee1153')
    version('2.0rc3',  sha256='05f347f5fa6b25d1ce5ec152a2407bbce033599eb6664f32f5331946eb3c7d66')

    variant('docs', default=False, description='Build the documentation')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-numpy@1.10:', type=('build', 'run'))
    depends_on('py-cython@0.29:', type=('build', 'run'))
    depends_on('py-sympy@0.7.6:1.0,1.1.1:', type=('build', 'run'))
    depends_on('py-pyparsing', type=('build', 'run'))
    depends_on('py-jinja2@2.7:', type=('build', 'run'))
    depends_on('py-setuptools@21:', type=('build', 'run'))
    depends_on('py-sphinx@1.5:', type=('build', 'run'), when='+docs')

    def build_args(self, spec, prefix):
        return ['--with-cython']
