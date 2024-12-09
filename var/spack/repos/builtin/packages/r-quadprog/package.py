# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQuadprog(RPackage):
    """Functions to Solve Quadratic Programming Problems.

    This package contains routines and documentation for solving quadratic
    programming problems."""

    cran = "quadprog"

    license("GPL-2.0-or-later")

    version("1.5-8", sha256="22128dd6b08d3516c44ff89276719ad4fe46b36b23fdd585274fa3a93e7a49cd")
    version("1.5-7", sha256="1af41e57df6f2d08ee8b72a1a5ada137beadb36c7ec9ab9bdb7c05226e8ae76d")
    version("1.5-6", sha256="1443e5ffdf884b13dd454e4f6aa260fce6ec47e6845d85b62238c206ce57dcba")
    version("1.5-5", sha256="d999620688354c283de5bb305203f5db70271b4dfdc23577cae8c2ba94c9e349")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("r@3.1.0:", type=("build", "run"))
