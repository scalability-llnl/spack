# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PySecretstorage(PythonPackage):
    """Python bindings to FreeDesktop.org Secret Service API."""

    homepage = "https://github.com/mitya57/secretstorage"
    url      = "https://pypi.io/packages/source/S/SecretStorage/SecretStorage-3.1.2.tar.gz"

    version('3.1.2', sha256='15da8a989b65498e29be338b3b279965f1b8f09b9668bd8010da183024c8bff6')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cryptography', type=('build', 'run'))
    depends_on('py-jeepney@0.4.2:', type=('build', 'run'))
