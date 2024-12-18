# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGlmgampoi(RPackage):
    """Fit a Gamma-Poisson Generalized Linear Model.

    Fit linear models to overdispersed count data.  The package can estimate
    the overdispersion and fit repeated models for matrix input. It is designed
    to handle large input datasets as they typically occur in single cell
    RNA-seq experiments."""

    bioc = "glmGamPoi"

    version("1.12.0", commit="5fdfa5ca1a56b19e51bc6e307ca6015cc56109a0")
    version("1.10.0", commit="048e17384209fc07031e09875ec6eea35e90ef46")
    version("1.8.0", commit="b723d61e05c1ad50a3cf6a6393ec3d97adc7edb4")

    depends_on("cxx", type="build")  # generated

    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-delayedmatrixstats", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-matrixgenerics", type=("build", "run"), when="@1.10.0:")
    depends_on("r-delayedarray", type=("build", "run"))
    depends_on("r-hdf5array", type=("build", "run"))
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-singlecellexperiment", type=("build", "run"), when="@1.10.0:")
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@1.10.0:")
    depends_on("r-vctrs", type=("build", "run"), when="@1.12.0:")
    depends_on("r-rcpparmadillo", type=("build", "run"))
    depends_on("r-beachmat", type=("build", "run"))
