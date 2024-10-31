# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcppml(RPackage):
    """Rcpp Machine Learning Library

    Fast machine learning algorithms including matrix factorization and
    divisive clustering for large sparse and dense matrices."""

    cran = "RcppML"

    version("0.3.7", sha256="325c6515085527eb9123cc5e87e028547065771ed4d623048f41886ae28908c6")

    depends_on("cxx", type="build")  # generated

    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-rcppeigen", type=("build", "run"))
