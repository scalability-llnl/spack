# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPy(PythonPackage):
    """Library with cross-python path, ini-parsing, io, code, log facilities"""

    homepage = "http://pylib.readthedocs.io/en/latest/"
    url      = "https://pypi.io/packages/source/p/py/py-1.8.0.tar.gz"

    version('1.8.0', sha256='dc639b046a6e2cff5bbe40194ad65936d6ba360b52b3c3fe1d08a82dd50b5e53')
    version('1.5.4',  sha256='3fd59af7435864e1a243790d322d763925431213b6b8529c6ca71081ace3bbf7')
    version('1.5.3',  sha256='29c9fab495d7528e80ba1e343b958684f4ace687327e6f789a94bf3d1915f881')
    version('1.4.33', sha256='1f9a981438f2acc20470b301a07a496375641f902320f70e31916fe3377385a9')
    version('1.4.31', sha256='a6501963c725fc2554dabfece8ae9a8fb5e149c0ac0a42fd2b02c5c1c57fc114')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
