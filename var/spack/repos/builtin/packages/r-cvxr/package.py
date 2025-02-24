# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCvxr(RPackage):
    """Disciplined Convex Optimization.

    An object-oriented modeling language for disciplined convex programming
    (DCP) as described in Fu, Narasimhan, and Boyd (2020,
    <doi:10.18637/jss.v094.i14>). It allows the user to formulate convex
    optimization problems in a natural way following mathematical convention
    and DCP rules. The system analyzes the problem, verifies its convexity,
    converts it into a canonical form, and hands it off to an appropriate
    solver to obtain the solution. Interfaces to solvers on CRAN and elsewhere
    are provided, both commercial and open source."""

    cran = "CVXR"

    license("Apache-2.0")

    version("1.0-14", sha256="4d027cc2b933720ded4edcc098fde1259992673825abdb109fd84fee4af57cdb")
    version("1.0-11", sha256="e92a9638f35f4909e2a29c3b7106081e3dae7ff88b14bb6466b87fbdc80b972a")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-rcpp@0.12.12:", type=("build", "run"))
    depends_on("r-bit64", type=("build", "run"))
    depends_on("r-clarabel@0.9.0:", type=("build", "run"), when="@1.0-14:")
    depends_on("r-gmp", type=("build", "run"))
    depends_on("r-rmpfr", type=("build", "run"))
    depends_on("r-ecosolver@0.5.4:", type=("build", "run"))
    depends_on("r-scs@3.0:", type=("build", "run"))
    depends_on("r-osqp", type=("build", "run"))
    depends_on("r-rcppeigen", type=("build", "run"))
