# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyS3transfer(PythonPackage):
    """S3transfer is a Python library for managing Amazon S3 transfers."""

    homepage = "https://github.com/boto/s3transfer"
    pypi = "s3transfer/s3transfer-0.2.1.tar.gz"

    version('0.3.4', sha256='7fdddb4f22275cf1d32129e21f056337fd2a80b6ccef1664528145b72c49e6d2')
    version('0.2.1', sha256='6efc926738a3cd576c2a79725fed9afde92378aa5c6a957e3af010cb019fac9d')

    depends_on('py-setuptools', type='build')
    depends_on('py-botocore@1.12.36:1.999', type=('build', 'run'))
    depends_on('py-futures@2.2:3', type=('build', 'run'), when='^python@:2')
