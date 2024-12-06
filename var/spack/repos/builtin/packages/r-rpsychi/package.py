# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRpsychi(RPackage):
    """Statistics for psychiatric research.

    The rpsychi offers a number of functions for psychiatry, psychiatric
    nursing, clinical psychology. Functions are primarily for statistical
    significance testing using published work. For example, you can conduct a
    factorial analysis of variance (ANOVA), which requires only the mean,
    standard deviation, and sample size for each cell, rather than the
    individual data. This package covers fundamental statistical tests such as
    t-test, chi-square test, analysis of variance, and multiple regression
    analysis. With some exceptions, you can obtain effect size and its
    confidence interval. These functions help you to obtain effect size from
    published work, and then to conduct a priori power analysis or
    meta-analysis, even if a researcher do not report effect size in a
    published work."""

    cran = "rpsychi"

    version("0.8", sha256="9c5465f59c92431e345418aee5bc1f5bc12f843492b20ccb9f92f3bdf19a80c0")

    depends_on("r-gtools", type=("build", "run"))
