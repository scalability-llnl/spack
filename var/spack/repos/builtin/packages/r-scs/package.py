# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScs(RPackage):
    """Splitting Conic Solver.

    Solves convex cone programs via operator splitting. Can solve: linear
    programs ('LPs'), second-order cone programs ('SOCPs'), semidefinite
    programs ('SDPs'), exponential cone programs ('ECPs'), and power cone
    programs ('PCPs'), or problems with any combination of those cones. 'SCS'
    uses 'AMD' (a set of routines for permuting sparse matrices prior to
    factorization) and 'LDL' (a sparse 'LDL' factorization and solve package)
    from 'SuiteSparse'
    (<https://people.engr.tamu.edu/davis/suitesparse.html>)."""

    cran = "scs"

    license("GPL-3.0-only")

    version("3.2.4", sha256="c3f39874bf4532fa8c2f2e2c41533ba4fe20b61cf6dfc6314407dc981621298f")
    version("3.0-1", sha256="d6881eeec7282f8bfbf60847327786e7f90299e4b8c0b084d8bd11fec7705913")

    depends_on("c", type="build")  # generated

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("gmake", type="build")
