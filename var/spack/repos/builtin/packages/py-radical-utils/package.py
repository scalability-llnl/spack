# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRadicalUtils(PythonPackage):
    """Shared code and tools for various RADICAL Projects"""

    homepage = "http://radical.rutgers.edu"
    url      = "https://pypi.io/packages/source/r/radical.utils/radical.utils-0.45.tar.gz"

    version('0.45', sha256='1333cff1a69532e51d4484fbac3fad6b172d415d2055a3141117c7cf8bdee6c5')
    version('0.41.1', sha256='582900e0434f49b69885a89bc65dc787362756e1014d52a4afac0bb61bcaa3ce')

    depends_on('py-setuptools', type='build')
    depends_on('py-colorama',   type=('build', 'run'))
    depends_on('py-netifaces',  type=('build', 'run'))
