# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsOauthlib(PythonPackage):
    """This project provides first-class OAuth library support for Requests.
    """

    homepage = "https://github.com/requests/requests-oauthlib"
    url      = "https://pypi.io/packages/source/r/requests-oauthlib/requests-oauthlib-1.2.0.tar.gz"

    version('1.2.0', sha256='bd6533330e8748e94bf0b214775fed487d309b8b8fe823dc45641ebcd9a32f57')
    version('0.3.3', sha256='37557b4de3eef50d2a4c65dc9382148b8331f04b1c637c414b3355feb0f007e9')

    depends_on('py-setuptools', type='build')
    depends_on('py-oauthlib@3.0.0:', type=('build', 'run'))
    depends_on('py-requests@2.0.0:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
