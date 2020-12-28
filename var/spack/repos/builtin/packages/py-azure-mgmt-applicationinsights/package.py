# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzureMgmtApplicationinsights(PythonPackage):
    """Microsoft Azure Application Insights Management Client Library for
    Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    url      = "https://pypi.io/packages/source/a/azure-mgmt-applicationinsights/azure-mgmt-applicationinsights-0.3.0.zip"

    version('0.3.0', sha256='3c788a54db4fbca1a8850151462ec1471ff59c86b3a10d6082952bbdaa7e6651')
    version('0.1.1', sha256='f10229eb9e3e9d0ad20188b8d14d67055e86f3815b43b75eedf96b654bee2a9b')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', when='@0.3:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', when='@0.3:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.20:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='@0.3: ^python@:2', type=('build', 'run'))
