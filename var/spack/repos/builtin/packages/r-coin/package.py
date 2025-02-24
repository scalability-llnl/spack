# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCoin(RPackage):
    """Conditional Inference Procedures in a Permutation Test Framework.

    Conditional inference procedures for the general independence problem
    including two-sample, K-sample (non-parametric ANOVA), correlation,
    censored, ordered and multivariate problems."""

    cran = "coin"

    license("GPL-2.0-only")

    version("1.4-3", sha256="8a6302dbf3ef570cd9f69ce7b6cd3d3b928dc776f840bbd767af132e0080b974")
    version("1.4-2", sha256="7546d1f27a82d98b4b3e43e4659eba0f74a67d5919ce85d2fb360282ba3cfbb2")
    version("1.3-1", sha256="5de2519a6e2b059bba9d74c58085cccaff1aaaa0454586ed164a108ebd1b2062")
    version("1.3-0", sha256="adcebb37e0a7dfddbf8ec1e09c12a809bd76d90b5b8ff2b1048a75252ba11ef8")
    version("1.2-2", sha256="d518065d3e1eb00121cb4e0200e1e4ae6b68eca6e249afc38bbffa35d24105bb")
    version("1.1-3", sha256="8b88ecc25903c83539dfc73cdc31a160e2aa4a7bea1773b22c79133d2f006035")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.3-0:")
    depends_on("r@3.6.0:", type=("build", "run"), when="@1.4-2:")
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-libcoin@1.0-0:", type=("build", "run"), when="@1.3-0:")
    depends_on("r-libcoin@1.0-9:", type=("build", "run"), when="@1.4-2:")
    depends_on("r-matrixstats@0.54.0:", type=("build", "run"), when="@1.3-0:")
    depends_on("r-modeltools@0.2-9:", type=("build", "run"))
    depends_on("r-mvtnorm@1.0-5:", type=("build", "run"))
    depends_on("r-multcomp", type=("build", "run"))
