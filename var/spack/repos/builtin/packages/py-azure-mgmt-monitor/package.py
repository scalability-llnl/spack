# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzureMgmtMonitor(PythonPackage):
    """Microsoft Azure Monitor Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    url      = "https://pypi.io/packages/source/a/azure-mgmt-monitor/azure-mgmt-monitor-0.11.0.zip"

    version('0.11.0', sha256='c6e1fe83dd2ddffa7f6d90c7aa63b3128042396a3893c14dc4816ad28cb15016')
    version('0.10.0', sha256='d57d604cc1a7a9ce35eb7cf8a00d4924887c688aa78dc035ea1f80066b297464')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
