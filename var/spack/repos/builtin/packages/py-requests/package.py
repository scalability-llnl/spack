# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequests(PythonPackage):
    """Python HTTP for Humans."""

    homepage = "http://python-requests.org"
    url = "https://pypi.io/packages/source/r/requests/requests-2.24.0.tar.gz"

    version('2.24.0', sha256='b3559a131db72c33ee969480840fff4bb6dd111de7dd27c8ee1f820f4f00231b')
    version('2.23.0', sha256='b3f43d496c6daba4493e7c431722aeb7dbc6288f52a6e04e7b6023b0247817e6')
    version('2.22.0', sha256='11e007a8a2aa0323f5a921e9e6a2d7e4e67d9877e85773fba9ba6419025cbeb4')
    version('2.21.0', sha256='502a824f31acdacb3a35b6690b5fbf0bc41d63a24a45c4004352b0242707598e')
    version('2.14.2', sha256='a274abba399a23e8713ffd2b5706535ae280ebe2b8069ee6a941cb089440d153')
    version('2.13.0', sha256='5722cd09762faa01276230270ff16af7acf7c5c45d623868d9ba116f15791ce8')
    version('2.11.1', sha256='5acf980358283faba0b897c73959cecf8b841205bb4b2ad3ef545f46eae1a133')
    version('2.3.0',  sha256='1c1473875d846fe563d70868acf05b1953a4472f4695b7b3566d1d978957b8fc')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-chardet@3.0.2:3.0.999', type=('build', 'run'), when='@2.16.0:2.22.999')
    depends_on('py-idna@2.5:2.8', type=('build', 'run'), when='@2.16.0:2.22.999')
    depends_on('py-chardet@3.0.2:3.999', type=('build', 'run'), when='@2.23.0:')
    depends_on('py-idna@2.5:2.999', type=('build', 'run'), when='@2.23.0:')
    depends_on('py-urllib3@1.21.1:1.24,1.25.2:1.25.999', type=('build', 'run'), when='@2.16.0:')
    depends_on('py-certifi@2017.4.17:', type=('build', 'run'), when='@2.16.0:')
