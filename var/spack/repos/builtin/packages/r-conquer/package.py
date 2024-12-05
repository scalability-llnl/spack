# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RConquer(RPackage):
    """Convolution-Type Smoothed Quantile Regression.

    Fast and accurate convolution-type smoothed quantile regression.
    Implemented using Barzilai-Borwein gradient descent with a Huber regression
    warm start. Construct confidence intervals for regression coefficients
    using multiplier bootstrap."""

    cran = "conquer"

    license("GPL-3.0-only")

    version("1.3.3", sha256="a2c6155ed74af0e2a279145843ec5229ae2f3707aa25169ae030c520aa97deba")
    version("1.3.1", sha256="14c28ab47b60c39696f34ee6fdd737bdcd2d28d05b3641c0e89960ab14a8bcd5")
    version("1.3.0", sha256="ac354e18c9ad6f41ed5200fad1c99fa5b124fc6fa5bba8f3434be2478f53d5fa")
    version("1.2.1", sha256="1354f90f962a2124e155227cdc0ed2c6e54682f1e08934c49a827e51dc112f45")
    version("1.0.2", sha256="542f6154ce1ffec0c1b4dd4e1f5b86545015f4b378c4c66a0840c65c57d674ff")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-rcpp@1.0.3:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-rcpparmadillo@0.9.850.1.0:", type=("build", "run"))

    depends_on("r-caret", type=("build", "run"), when="@1.2.1")
