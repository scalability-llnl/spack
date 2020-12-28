# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzureMgmtBatch(PythonPackage):
    """Microsoft Azure Batch Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    url      = "https://pypi.io/packages/source/a/azure-mgmt-batch/azure-mgmt-batch-9.0.0.zip"

    version('9.0.0', sha256='03417eecfa1fac906e674cb1cb43ed7da27a96277277b091d7c389ba39f6c3fe')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
