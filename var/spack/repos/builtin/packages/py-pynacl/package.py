# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPynacl(PythonPackage):
    """Python binding to the Networking and Cryptography (NaCl) library."""

    homepage = "https://github.com/pyca/pynacl/"
    url      = "https://pypi.io/packages/source/P/PyNaCl/PyNaCl-1.4.0.tar.gz"

    version('1.4.0', sha256='54e9a2c849c742006516ad56a88f5c74bf2ce92c9f67435187c3c5953b346505')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-cffi@1.4.1:', type=('build', 'run'))
