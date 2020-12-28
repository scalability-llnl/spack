# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEarthengineApi(PythonPackage):
    """This package allows developers to interact with Google Earth Engine
    using the Python programming language."""

    homepage = "https://github.com/google/earthengine-api"
    url      = "https://pypi.io/packages/source/e/earthengine-api/earthengine-api-0.1.186.tar.gz"

    version('0.1.186', sha256='ced86dc969f5db13eea91944e29c39146bacbb7026a46f4b4ac349b365979627')

    depends_on('py-setuptools', type='build')
    depends_on('py-google-api-python-client', type=('build', 'run'))
    depends_on('py-google-auth@1.4.1:', type=('build', 'run'))
    depends_on('py-google-auth-httplib2@0.0.3:', type=('build', 'run'))
    depends_on('py-httplib2@0.9.2:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
