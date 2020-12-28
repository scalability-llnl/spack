# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastcache(PythonPackage):
    """C implementation of Python 3 functools.lru_cache"""

    homepage = "https://github.com/pbrady/fastcache"
    url      = "https://pypi.io/packages/source/f/fastcache/fastcache-1.1.0.tar.gz"

    version('1.1.0', sha256='6de1b16e70335b7bde266707eb401a3aaec220fb66c5d13b02abf0eab8be782b')

    depends_on('py-setuptools', type='build')
