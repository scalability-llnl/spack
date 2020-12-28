# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTyping(PythonPackage):
    """This is a backport of the standard library typing module to Python
    versions older than 3.6."""

    homepage = "https://docs.python.org/3/library/typing.html"
    url      = "https://pypi.io/packages/source/t/typing/typing-3.7.4.1.tar.gz"

    version('3.7.4.1', sha256='91dfe6f3f706ee8cc32d38edbbf304e9b7583fb37108fef38229617f8b3eba23')
    version('3.6.6', sha256='4027c5f6127a6267a435201981ba156de91ad0d1d98e9ddc2aa173453453492d')
    version('3.6.4', sha256='d400a9344254803a2368533e4533a4200d21eb7b6b729c173bc38201a74db3f2')
    version('3.6.1', sha256='c36dec260238e7464213dcd50d4b5ef63a507972f5780652e835d0228d0edace')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
