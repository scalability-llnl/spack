# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUvloop(PythonPackage):
    """uvloop is a fast, drop-in replacement of the built-in asyncio event"""

    homepage = "http://github.com/MagicStack/uvloop"
    url      = "https://pypi.io/packages/source/u/uvloop/uvloop-0.14.0.tar.gz"

    version('0.14.0', sha256='123ac9c0c7dd71464f58f1b4ee0bbd81285d96cdda8bc3519281b8973e3a461e')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
