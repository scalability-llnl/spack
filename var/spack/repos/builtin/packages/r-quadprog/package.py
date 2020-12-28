# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQuadprog(RPackage):
    """This package contains routines and documentation for solving
       quadratic programming problems."""

    homepage = "https://cloud.r-project.org/package=quadprog"
    url      = "https://cloud.r-project.org/src/contrib/quadprog_1.5-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/quadprog"

    version('1.5-7', sha256='1af41e57df6f2d08ee8b72a1a5ada137beadb36c7ec9ab9bdb7c05226e8ae76d')
    version('1.5-6', sha256='1443e5ffdf884b13dd454e4f6aa260fce6ec47e6845d85b62238c206ce57dcba')
    version('1.5-5', sha256='d999620688354c283de5bb305203f5db70271b4dfdc23577cae8c2ba94c9e349')

    depends_on('r@3.1.0:', type=('build', 'run'))
