# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJaracoFunctools(PythonPackage):
    """Functools like those found in stdlib"""

    homepage = "https://github.com/jaraco/jaraco.functools"
    url      = "https://pypi.io/packages/source/j/jaraco.functools/jaraco.functools-2.0.tar.gz"

    version(
        '2.0', sha256='35ba944f52b1a7beee8843a5aa6752d1d5b79893eeb7770ea98be6b637bf9345')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@1.15.0:', type='build')
    depends_on('py-backports-functools-lru-cache@1.0.3:',
               when='^python@:2', type=('build', 'run'))
    depends_on('py-more-itertools', type=('build', 'run'))
    depends_on('python@2.7:', type=('build', 'run'))
