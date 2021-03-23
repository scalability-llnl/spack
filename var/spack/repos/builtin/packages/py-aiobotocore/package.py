# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAiobotocore(PythonPackage):
    """Async client for amazon services using botocore and aiohttp/asyncio."""

    homepage = "https://aiobotocore.readthedocs.io/en/latest/"
    pypi = "aiobotocore/aiobotocore-1.2.1.tar.gz"

    version('1.2.1', sha256='58cc422e65fc89f7cb78eca740d241ac8e15f39f6b308cc23152711e8a987d45')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-botocore@1.19.52', type=('build', 'run'))
    depends_on('py-aiohttp@3.3.1:', type=('build', 'run'))
    depends_on('py-wrapt@1.10.10:', type=('build', 'run'))
    depends_on('py-aioitertools@0.5.1:', type=('build', 'run'))
