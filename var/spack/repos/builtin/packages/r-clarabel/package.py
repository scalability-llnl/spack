# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RClarabel(RPackage):
    """A versatile interior point solver that solves linear programs (LPs),
    quadratic programs (QPs), second-order cone programs (SOCPs), semidefinite
    programs (SDPs), and problems with exponential and power cone constraints
    (<https://clarabel.org/stable/>). For quadratic objectives, unlike interior
    point solvers based on the standard homogeneous self-dual embedding (HSDE)
    model, 'Clarabel' handles quadratic objective without requiring any
    epigraphical reformulation of its objective function. It can therefore
    be significantly faster than other HSDE-based solvers for problems with
    quadratic objective functions. Infeasible problems are detected using using
    a homogeneous embedding technique."""

    homepage = "https://oxfordcontrol.github.io/clarabel-r/"
    cran = "clarabel"

    license("Apache-2.0", checked_by="wdconinc")

    version("0.9.0", sha256="50963022f8e5dc9d956193acf7b87194548dc4b3555bd844aa1f9f4d34f2c6bc")

    depends_on("rust", type=("build", "run"))
