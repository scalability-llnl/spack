# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzureMgmtCore(PythonPackage):
    """Microsoft Azure Management Core Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/core/azure-mgmt-core"
    url      = "https://pypi.io/packages/source/a/azure-mgmt-core/azure-mgmt-core-1.2.0.zip"

    version('1.2.0', sha256='8fe3b59446438f27e34f7b24ea692a982034d9e734617ca1320eedeee1939998')
    version('1.0.0', sha256='510faf49a10daec8346cc086143d8e667ef3b4f8c8022a8e710091027631a55e')

    depends_on('py-setuptools', type='build')
    depends_on('py-azure-core@1.7.0:1.999', when='@1.2:', type=('build', 'run'))
    depends_on('py-azure-core@1.4.0:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
    depends_on('py-typing', when='^python@:3.4', type=('build', 'run'))
