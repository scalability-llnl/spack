# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzureCore(PythonPackage):
    """Microsoft Azure Core Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/core/azure-core"
    url      = "https://pypi.io/packages/source/a/azure-core/azure-core-1.7.0.zip"

    version('1.7.0', sha256='a66da240a287f447f9867f54ba09ea235895cec13ea38c5f490ce4eedefdd75c')
    version('1.6.0', sha256='d10b74e783cff90d56360e61162afdd22276d62dc9467e657ae866449eae7648')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.18.4:', type=('build', 'run'))
    depends_on('py-six@1.6:', type=('build', 'run'))
    depends_on('py-azure-nspkg', when='^python@:2', type=('build', 'run'))
    depends_on('py-enum34@1.0.4:', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-typing', when='^python@:3.4', type=('build', 'run'))
