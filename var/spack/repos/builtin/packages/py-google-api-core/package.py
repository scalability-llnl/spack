# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleApiCore(PythonPackage):
    """Google API client core library."""

    homepage = "https://github.com/GoogleCloudPlatform/google-cloud-python"
    url      = "https://pypi.io/packages/source/g/google-api-core/google-api-core-1.14.2.tar.gz"

    # google.api_core.operations_v1 and google.api_core.gapic_v1 require
    # grpc optional dependency
    import_modules = ['google.api_core', 'google.api_core.future']

    version('1.14.2', sha256='2c23fbc81c76b941ffb71301bb975ed66a610e9b03f918feacd1ed59cf43a6ec')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-googleapis-common-protos@1.6:1.999', type=('build', 'run'))
    depends_on('py-protobuf@3.4.0:', type=('build', 'run'))
    depends_on('py-google-auth@0.4:1.999', type=('build', 'run'))
    depends_on('py-requests@2.18:2.999', type=('build', 'run'))
    depends_on('py-setuptools@34.0.0:', type=('build', 'run'))
    depends_on('py-six@1.10.0:', type=('build', 'run'))
    depends_on('py-pytz', type=('build', 'run'))
    depends_on('py-futures@3.2.0:', type=('build', 'run'), when='^python@:3.1')
