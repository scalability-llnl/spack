# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleApiPythonClient(PythonPackage):
    """The Google API Client for Python is a client library for accessing the
    Plus, Moderator, and many other Google APIs."""

    homepage = "http://github.com/google/google-api-python-client/"
    url      = "https://pypi.io/packages/source/g/google-api-python-client/google-api-python-client-1.7.10.tar.gz"

    version('1.7.10', sha256='2e55a5c7b56233c68945b6804c73e253445933f4d485d4e69e321b38772b9dd6')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-httplib2@0.9.2:', type=('build', 'run'))
    depends_on('py-google-auth@1.4.1:', type=('build', 'run'))
    depends_on('py-google-auth-httplib2@0.0.3:', type=('build', 'run'))
    depends_on('py-six@1.6.1:', type=('build', 'run'))
    depends_on('py-uritemplate@3.0.0:', type=('build', 'run'))
