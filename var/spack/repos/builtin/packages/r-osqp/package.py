# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROsqp(RPackage):
    """Quadratic Programming Solver using the 'OSQP' Library.

    Provides bindings to the 'OSQP' solver. The 'OSQP' solver is a numerical
    optimization package or solving convex quadratic programs written in 'C'
    and based on the alternating direction method of multipliers. See
    <arXiv:1711.08013> for details."""

    cran = "osqp"

    license("Apache-2.0 OR custom")

    version("0.6.3.3", sha256="ff3d8e4ec7764333144d461eb5ea7a4adbf5b5f29f84c3ec3e60a93802e2f5bb")
    version("0.6.0.8", sha256="14034045ae4ae5ec4eae4944653d41d94282fa85a0cd53614ac86f34fd02ed97")
    version("0.6.0.7", sha256="ee6584d02341e3f1d8fab3b2cb93defd6c48d561297d82a6bedb3e7541868203")

    depends_on("r-rcpp@0.12.14:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-matrix@1.6-1:", type=("build", "run"), when="@0.6.3:")
    depends_on("r-r6", type=("build", "run"))
    depends_on("cmake", type="build")
