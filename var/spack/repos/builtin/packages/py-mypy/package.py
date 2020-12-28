# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMypy(PythonPackage):
    """Optional static typing for Python."""

    homepage = "http://www.mypy-lang.org/"
    url      = "https://pypi.io/packages/source/m/mypy/mypy-0.740.tar.gz"

    version('0.740', sha256='48c8bc99380575deb39f5d3400ebb6a8a1cb5cc669bbba4d3bb30f904e0a0e7d')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-typed-ast@1.4.0:1.4.999', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7.4:', type=('build', 'run'))
    depends_on('py-mypy-extensions@0.4.0:0.4.999', type=('build', 'run'))
