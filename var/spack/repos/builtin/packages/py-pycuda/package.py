# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPycuda(PythonPackage):
    """"""

    homepage = "https://mathema.tician.de/software/pycuda/"
    url      = "https://pypi.io/packages/source/p/pycuda/pycuda-2019.1.2.tar.gz"

    version('2019.1.2', sha256='ada56ce98a41f9f95fe18809f38afbae473a5c62d346cfa126a2d5477f24cc8a')
    version('2016.1.2', sha256='a7dbdac7e2f0c0d2ad98f5f281d5a9d29d6673b3c20210e261b96e9a2d0b6e37')

    depends_on('py-setuptools', type='build')
    depends_on('cuda')
    depends_on('boost')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-six', type='run')
    depends_on('py-decorator', type='run')

    depends_on('cuda@:8.0.61', when='@2016.1.2')
