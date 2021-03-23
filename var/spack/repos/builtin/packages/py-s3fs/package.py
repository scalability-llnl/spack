# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyS3fs(PythonPackage):
    """S3FS builds on aiobotocore to provide a convenient Python filesystem
    interface for S3."""

    homepage = "https://s3fs.readthedocs.io/en/latest/"
    pypi = "s3fs/s3fs-0.5.2.tar.gz"

    version('0.5.2', sha256='87e5210415db17b9de18c77bcfc4a301570cc9030ee112b77dc47ab82426bae1')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-aiobotocore@1.0.1:', type=('build', 'run'))
    depends_on('py-fsspec@0.8.0:', type=('build', 'run'))
