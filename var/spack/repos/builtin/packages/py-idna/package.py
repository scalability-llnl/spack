# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack.package import *


class PyIdna(PythonPackage):
    """Internationalized Domain Names for Python (IDNA 2008 and UTS #46) """

    homepage = "https://github.com/kjd/idna"
    url      = "https://pypi.io/packages/source/i/idna/idna-2.8.tar.gz"

    version('2.8', sha256='c357b3f628cf53ae2c4c05627ecc484553142ca23264e593d327bcde5e9c3407')
    version('2.5', sha256='3cb5ce08046c4e3a560fc02f138d0ac63e00f8ce5901a56b32ec8b7994082aab')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'link'))
