# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyJsmin(PythonPackage):
    """JavaScript minifier."""

    homepage = "https://github.com/tikitu/jsmin/"
    url      = "https://pypi.io/packages/source/j/jsmin/jsmin-2.2.2.tar.gz"

    version('2.2.2', sha256='b6df99b2cd1c75d9d342e4335b535789b8da9107ec748212706ef7bbe5c2553b')

    depends_on('py-setuptools', type='build')
