# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChardet(PythonPackage):
    """Universal encoding detector for Python 2 and 3"""

    homepage = "https://github.com/chardet/chardet"
    url      = "https://pypi.io/packages/source/c/chardet/chardet-3.0.4.tar.gz"

    version('3.0.4', sha256='84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae')
    version('3.0.2', sha256='4f7832e7c583348a9eddd927ee8514b3bf717c061f57b21dbe7697211454d9bb')
    version('2.3.0', sha256='e53e38b3a4afe6d1132de62b7400a4ac363452dc5dfcf8d88e8e0cce663c68aa')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pytest-runner', type='build')
