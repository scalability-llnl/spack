# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyMsrest(PythonPackage):
    """AutoRest swagger generator Python client runtime."""

    homepage = "https://github.com/Azure/msrest-for-python"
    url      = "https://pypi.io/packages/source/m/msrest/msrest-0.6.16.tar.gz"

    version('0.6.16', sha256='214c5be98954cb45feb6a6a858a7ae6d41a664e80294b65db225bbaa33d9ca3c')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.16:2.999', type=('build', 'run'))
    depends_on('py-requests-oauthlib@0.5.0:', type=('build', 'run'))
    depends_on('py-isodate@0.6.0:', type=('build', 'run'))
    depends_on('py-certifi@2017.4.17:', type=('build', 'run'))
    depends_on('py-enum34@1.0.4:', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-typing', when='^python@:3.4', type=('build', 'run'))
