# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzureMgmtMsi(PythonPackage):
    """Microsoft Azure MSI Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    url      = "https://pypi.io/packages/source/a/azure-mgmt-msi/azure-mgmt-msi-1.0.0.zip"

    version('1.0.0', sha256='d46f3aab25db3dad520e4055c1d67afe4fcc6d66335c762134e60f82265f8f58')
    version('0.2.0', sha256='8622bc9a164169a0113728ebe7fd43a88189708ce6e10d4507247d6907987167')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', when='@1:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', when='@1:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.27:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='@1: ^python@:2', type=('build', 'run'))
