# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetworkx(PythonPackage):
    """NetworkX is a Python package for the creation, manipulation, and study
    of the structure, dynamics, and functions of complex networks."""

    homepage = "http://networkx.github.io/"
    url      = "https://pypi.io/packages/source/n/networkx/networkx-2.4.tar.gz"

    version('2.4',  sha256='f8f4ff0b6f96e4f9b16af6b84622597b5334bf9cae8cf9b2e42e7985d5c95c64')
    version('2.3',  sha256='8311ddef63cf5c5c5e7c1d0212dd141d9a1fe3f474915281b73597ed5f1d4e3d')
    version('2.2',  sha256='45e56f7ab6fe81652fb4bc9f44faddb0e9025f469f602df14e3b2551c2ea5c8b')
    version('2.1',  sha256='64272ca418972b70a196cb15d9c85a5a6041f09a2f32e0d30c0255f25d458bb1')
    version('2.0',  sha256='cd5ff8f75d92c79237f067e2f0876824645d37f017cfffa5b7c9678cae1454aa')
    version('1.11', sha256='0d0e70e10dfb47601cbb3425a00e03e2a2e97477be6f80638fef91d54dd1e4b8')
    version('1.10', sha256='ced4095ab83b7451cec1172183eff419ed32e21397ea4e1971d92a5808ed6fb8')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('python@3.5:', type=('build', 'run'), when='@2.3:')
    depends_on('py-setuptools', type='build')
    depends_on('py-decorator@3.4.0:', type=('build', 'run'))
    depends_on('py-decorator@4.1.0:', type=('build', 'run'), when='@2.0:')
    depends_on('py-decorator@4.3.0:', type=('build', 'run'), when='@2.2:')

    def url_for_version(self, version):
        ext = 'tar.gz'
        if Version('2.0') <= version <= Version('2.3'):
            ext = 'zip'

        url = 'https://pypi.io/packages/source/n/networkx/networkx-{0}.{1}'
        return url.format(version, ext)
