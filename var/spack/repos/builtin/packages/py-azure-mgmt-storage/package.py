# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzureMgmtStorage(PythonPackage):
    """Microsoft Azure Storage Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    url      = "https://pypi.io/packages/source/a/azure-mgmt-storage/azure-mgmt-storage-11.1.0.zip"

    version('11.1.0', sha256='ef23587c1b6dc0866ebf0e91e83ba05d7f7e4fea7951b704781b9cd9f5f27f1c')
    version('11.0.0', sha256='f9791c2a84eee0a55bbf757632a2a4d1e102db958e75422d5e0e7306041129b8')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
