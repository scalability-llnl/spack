# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyMonotonic(PythonPackage):
    """An implementation of time.monotonic() for Python 2 & < 3.3"""

    pypi = "monotonic/monotonic-1.2.tar.gz"

    version('1.2', sha256='c0e1ceca563ca6bb30b0fb047ee1002503ae6ad3585fc9c6af37a8f77ec274ba')

    depends_on('py-setuptools', type='build')
