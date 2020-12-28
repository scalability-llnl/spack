# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsFunctoolsLruCache(PythonPackage):
    """Backport of functools.lru_cache from Python 3.3"""

    homepage = "https://github.com/jaraco/backports.functools_lru_cache"
    url = "https://pypi.io/packages/source/b/backports.functools_lru_cache/backports.functools_lru_cache-1.4.tar.gz"

    py_namespace = 'backports'

    version('1.5', sha256='9d98697f088eb1b0fa451391f91afb5e3ebde16bbdb272819fd091151fda4f1a')
    version('1.4', sha256='31f235852f88edc1558d428d890663c49eb4514ffec9f3650e7f3c9e4a12e36f')
    version('1.0.1', sha256='593275768571eb2bcfe0795a30108f8a0e85e14e98c3a5e498e789f891d82f3d',
            url="https://pypi.io/packages/source/b/backports.functools_lru_cache/backports.functools_lru_cache-1.0.1.zip")

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@1.15.0:', type='build')
    depends_on('python@2.6.0:3.3.99',        type=('build', 'run'))
