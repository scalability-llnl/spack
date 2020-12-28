# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonschema(PythonPackage):
    """Jsonschema: An(other) implementation of JSON Schema for Python."""

    homepage = "http://github.com/Julian/jsonschema"
    url      = "https://pypi.io/packages/source/j/jsonschema/jsonschema-3.2.0.tar.gz"

    version('3.2.0', sha256='c8a85b28d377cc7737e46e2d9f2b4f44ee3c0e1deac6bf46ddefc7187d30797a')
    version('3.1.1', sha256='2fa0684276b6333ff3c0b1b27081f4b2305f0a36cf702a23db50edb141893c3f')
    version('3.0.2', sha256='8d4a2b7b6c2237e0199c8ea1a6d3e05bf118e289ae2b9d7ba444182a2959560d')
    version('3.0.1', sha256='0c0a81564f181de3212efa2d17de1910f8732fa1b71c42266d983cd74304e20d')
    version('2.6.0', sha256='6ff5f3180870836cae40f06fa10419f557208175f13ad7bc26caa77beb1f6e02')
    version('2.5.1', sha256='36673ac378feed3daa5956276a829699056523d7961027911f064b52255ead41')

    depends_on('python@2.6:2.8,3.4:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@3:', type=('build', 'run'))

    depends_on('py-setuptools', type='build', when='@:2')
    depends_on('py-setuptools', type=('build', 'run'), when='@3:')
    depends_on('py-vcversioner', type='build', when='@:2')
    depends_on('py-setuptools-scm', type='build', when='@3:')

    depends_on('py-functools32', when="^python@:2", type=('build', 'run'))
    depends_on('py-attrs@17.4.0:', when='@3:', type=('build', 'run'))
    depends_on('py-pyrsistent@0.14.0:', when='@3:', type=('build', 'run'))
    depends_on('py-six@1.11.0:', when='@3:', type=('build', 'run'))

    depends_on('py-importlib-metadata', when='@3.1.1: ^python@:3.7.99', type=('build', 'run'))
