# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyNestAsyncio(PythonPackage):
    """Patch asyncio to allow nested event loops."""

    homepage = "https://github.com/erdewit/nest_asyncio"
    url      = "https://pypi.io/packages/source/n/nest-asyncio/nest_asyncio-1.4.0.tar.gz"

    version('1.4.0', sha256='5773054bbc14579b000236f85bc01ecced7ffd045ec8ca4a9809371ec65a59c8')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
