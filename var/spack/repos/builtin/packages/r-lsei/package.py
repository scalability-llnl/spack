# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLsei(RPackage):
    """Solving Least Squares or Quadratic Programming Problems under
    Equality/Inequality Constraints.

    It contains functions that solve least squares linear regression problems
    under linear equality/inequality constraints. Functions for solving
    quadratic programming problems are also available, which transform such
    problems into least squares ones first. It is developed based on the
    'Fortran' program of Lawson and Hanson (1974, 1995), which is public domain
    and available at <http://www.netlib.org/lawson-hanson>."""

    cran = "lsei"

    license("GPL-2.0-or-later")

    version("1.3-0", sha256="6289058f652989ca8a5ad6fa324ce1762cc9e36c42559c00929b70f762066ab6")
    version("1.2-0", sha256="4781ebd9ef93880260d5d5f23066580ac06061e95c1048fb25e4e838963380f6")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated
