# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyPytestTimeout(PythonPackage):
    """A plugin which will terminate tests after a certain timeout,
       assuming the test session isn't being debugged."""

    homepage = "https://github.com/pytest-dev/pytest-timeout/"
    pypi     = "pytest-timeout/pytest-timeout-1.4.2.tar.gz"

    version('1.4.2', sha256='20b3113cf6e4e80ce2d403b6fb56e9e1b871b510259206d40ff8d609f48bda76')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest@3.6.0:', type=('build', 'run'))
