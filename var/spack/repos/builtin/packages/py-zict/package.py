# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZict(PythonPackage):
    """Mutable mapping tools"""

    homepage = "http://zict.readthedocs.io/en/latest/"
    url      = "https://pypi.io/packages/source/z/zict/zict-1.0.0.tar.gz"

    version('1.0.0', sha256='e34dd25ea97def518fb4c77f2c27078f3a7d6c965b0a3ac8fe5bdb0a8011a310')

    depends_on('py-setuptools', type='build')
    depends_on('py-heapdict', type=('build', 'run'))
