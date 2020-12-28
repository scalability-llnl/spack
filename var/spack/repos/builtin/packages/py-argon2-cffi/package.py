# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyArgon2Cffi(PythonPackage):
    """The secure Argon2 password hashing algorithm.."""

    homepage = "https://argon2-cffi.readthedocs.io/"
    url      = "https://pypi.io/packages/source/a/argon2-cffi/argon2-cffi-20.1.0.tar.gz"

    version('20.1.0', sha256='d8029b2d3e4b4cea770e9e5a0104dd8fa185c1724a0f01528ae4826a6d25f97d')

    depends_on('py-setuptools', type='build')
    depends_on('py-cffi@1.0.0:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-enum34', when='^python@:3.3', type=('build', 'run'))
