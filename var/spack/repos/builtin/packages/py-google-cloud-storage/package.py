# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudStorage(PythonPackage):
    """Google Cloud Storage API client library."""

    homepage = "https://github.com/GoogleCloudPlatform/google-cloud-python"
    url      = "https://pypi.io/packages/source/g/google-cloud-storage/google-cloud-storage-1.18.0.tar.gz"

    version('1.18.0', sha256='9fb3dc68948f4c893c2b16f5a3db3daea2d2f3b8e9d5c2d505fe1523758009b6')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-google-auth@1.2.0:', type=('build', 'run'))
    depends_on('py-google-cloud-core@1.0:1.999', type=('build', 'run'))
    depends_on('py-google-resumable-media@0.3.1:', type=('build', 'run'))
