# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzureKeyvaultCertificates(PythonPackage):
    """Microsoft Azure Key Vault Certificates Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-certificates"
    url      = "https://pypi.io/packages/source/a/azure-keyvault-certificates/azure-keyvault-certificates-4.1.0.zip"

    version('4.1.0', sha256='544f56480619e1db350f2e7b117b22af778e02174bd6bcb0af9ae00c50353419')

    depends_on('py-setuptools', type='build')
    depends_on('py-azure-core@1.2.1:1.999', type=('build', 'run'))
    depends_on('py-msrest@0.6.0:', type=('build', 'run'))
    depends_on('py-azure-keyvault-nspkg', when='^python@:2', type=('build', 'run'))
    depends_on('py-enum34@1.0.4:', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-typing', when='^python@:3.4', type=('build', 'run'))
