# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUcminf(RPackage):
    """General-Purpose Unconstrained Non-Linear Optimization.

    An algorithm for general-purpose unconstrained non-linear optimization.
    The algorithm is of quasi-Newton type with BFGS updating of the inverse
    Hessian and soft line search with a trust region type monitoring of the
    input to the line search algorithm. The interface of 'ucminf' is designed
    for easy interchange with 'optim'."""

    cran = "ucminf"

    license("GPL-2.0-or-later")

    version("1.2.2", sha256="4bdb6ae769fa49a167cfdc92dc544ba3b6f34df6c08810cfb0c55613aff5bd29")
    version("1.1-4.1", sha256="01a5b6f373ad267d22e2c29b8f7b6e31a1a148e48f4413e6a38e51aa049976b2")
    version("1.1-4", sha256="a2eb382f9b24e949d982e311578518710f8242070b3aa3314a331c1e1e7f6f07")

    depends_on("r@3.5.0:", when="@1.2.0:", type=("build", "run"))
