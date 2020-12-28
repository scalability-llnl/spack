# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAiofiles(PythonPackage):
    """aiofiles is an Apache2 licensed library, written in Python, for
    handling local disk files in asyncio applications."""

    homepage = "https://github.com/Tinche/aiofiles"
    url      = "https://pypi.io/packages/source/a/aiofiles/aiofiles-0.5.0.tar.gz"

    version('0.5.0', sha256='98e6bcfd1b50f97db4980e182ddd509b7cc35909e903a8fe50d8849e02d815af')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
