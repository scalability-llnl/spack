# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyMacholib(PythonPackage):
    """Python package for Mach-O header analysis and editing"""

    pypi = "macholib/macholib-1.11.tar.gz"

    version('1.11', 'c4180ffc6f909bf8db6cd81cff4b6f601d575568f4d5dee148c830e9851eb9db')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-altgraph', type=('build', 'run'))
