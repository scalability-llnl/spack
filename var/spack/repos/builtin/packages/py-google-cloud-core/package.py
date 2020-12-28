# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudCore(PythonPackage):
    """Google Cloud API client core library."""

    homepage = "https://github.com/GoogleCloudPlatform/google-cloud-python"
    url      = "https://pypi.io/packages/source/g/google-cloud-core/google-cloud-core-1.0.3.tar.gz"

    version('1.0.3', sha256='10750207c1a9ad6f6e082d91dbff3920443bdaf1c344a782730489a9efa802f1')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-google-api-core@1.14:1.999', type=('build', 'run'))
