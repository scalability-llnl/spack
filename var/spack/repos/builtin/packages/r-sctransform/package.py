# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSctransform(RPackage):
    """Variance Stabilizing Transformations for Single Cell UMI Data.

    A normalization method for single-cell UMI count data using a variance
    stabilizing transformation. The transformation is based on a negative
    binomial regression model with regularized parameters. As part of the same
    regression framework, this package also provides functions for batch
    correction, and data correction. See Hafemeister and Satija 2019
    <doi:10.1101/576827> for more details."""

    cran = "sctransform"

    license("GPL-3.0-only OR custom")

    version("0.4.1", sha256="5f6be7f8be543e4c32c8007207b603a750881459370b7bb5afd63e8c8fabf171")
    version("0.3.5", sha256="c08e56df05d64ed04ee53eb9e1d4d321da8aff945e36d56db1d5ceb1cd7e6e0b")
    version("0.3.3", sha256="83af125c40f211e1ddae5098f88766aea1453c02ae98486081f3efadb3620b2b")
    version("0.3.2", sha256="5dbb0a045e514c19f51bbe11c2dba0b72dca1942d6eb044c36b0538b443475dc")
    version("0.2.0", sha256="d7f4c7958693823454f1426b23b0e1e9c207ad61a7a228602a1885a1318eb3e4")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.1.0:", type=("build", "run"), when="@0.3.2:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.3.3:")
    depends_on("r@3.6.0:", type=("build", "run"), when="@0.4.0:")
    depends_on("r-dplyr", type=("build", "run"), when="@0.3.3:")
    depends_on("r-magrittr", type=("build", "run"), when="@0.3.3:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-matrix@1.5-0:", type=("build", "run"), when="@0.3.5:")
    depends_on("r-future-apply", type=("build", "run"))
    depends_on("r-future", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@0.3.3:")
    depends_on("r-gridextra", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"), when="@0.3.2:")
    depends_on("r-rcpparmadillo", type=("build", "run"), when="@0.3.2:")
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))

    depends_on("r-rcppeigen", type=("build", "run"), when="@:0.2.0")
