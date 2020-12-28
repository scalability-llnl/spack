# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCachetools(PythonPackage):
    """This module provides various memoizing collections and decorators,
    including variants of the Python 3 Standard Library @lru_cache function
    decorator."""

    homepage = "https://github.com/tkem/cachetools"
    url      = "https://pypi.io/packages/source/c/cachetools/cachetools-3.1.1.tar.gz"

    version('3.1.1', sha256='8ea2d3ce97850f31e4a08b0e2b5e6c34997d7216a9d2c98e0f3978630d4da69a')

    depends_on('py-setuptools', type='build')
