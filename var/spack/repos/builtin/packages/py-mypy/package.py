# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyMypy(PythonPackage):
    """Optional static typing for Python."""

    homepage = "http://www.mypy-lang.org/"
    pypi = "mypy/mypy-0.740.tar.gz"

    version('0.800', sha256='e0202e37756ed09daf4b0ba64ad2c245d357659e014c3f51d8cd0681ba66940a')
    version('0.740', sha256='48c8bc99380575deb39f5d3400ebb6a8a1cb5cc669bbba4d3bb30f904e0a0e7d')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-typed-ast@1.4.0:1.4.999', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7.4:', type=('build', 'run'))
    depends_on('py-mypy-extensions@0.4.3:0.4.999', type=('build', 'run'))
