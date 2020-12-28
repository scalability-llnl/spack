# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzureMgmtCognitiveservices(PythonPackage):
    """Microsoft Azure Cognitive Services Management Client Library for
    Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    url      = "https://pypi.io/packages/source/a/azure-mgmt-cognitiveservices/azure-mgmt-cognitiveservices-6.2.0.zip"

    version('6.2.0', sha256='93503507ba87c18fe24cd3dfcd54e6e69a4daf7636f38b7537e09cee9a4c13ce')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
