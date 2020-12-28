# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzureCliNspkg(PythonPackage):
    """Microsoft Azure CLI Namespace Package."""

    homepage = "https://github.com/Azure/azure-cli"
    url      = "https://pypi.io/packages/source/a/azure-cli-nspkg/azure-cli-nspkg-3.0.4.tar.gz"

    version('3.0.4', sha256='1bde56090f548c6435bd3093995cf88e4c445fb040604df8b5b5f70780d79181')

    depends_on('py-setuptools', type='build')
    depends_on('py-azure-nspkg@2.0.0:', type=('build', 'run'))
