# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAsyncTimeout(PythonPackage):
    """asyncio-compatible timeout context manager."""

    homepage = "https://github.com/aio-libs/async-timeout"
    url      = "https://github.com/aio-libs/async-timeout/archive/v3.0.1.tar.gz"

    version('3.0.1', sha256='d0a7a927ed6b922835e1b014dfcaa9982caccbb25131320582cc660af7c93949')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.5.3:', type=('build', 'run'))
