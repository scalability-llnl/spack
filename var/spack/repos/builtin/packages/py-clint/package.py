# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClint(PythonPackage):
    """Python Command-line Application Tools"""

    homepage = "https://github.com/kennethreitz-archive/clint"
    url      = "https://pypi.io/packages/source/c/clint/clint-0.5.1.tar.gz"

    version('0.5.1', sha256='05224c32b1075563d0b16d0015faaf9da43aa214e4a2140e51f08789e7a4c5aa')

    depends_on('py-setuptools', type='build')
    depends_on('py-args', type=('build', 'run'))
