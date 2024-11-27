# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRocr(RPackage):
    """Visualizing the Performance of Scoring Classifiers.

    ROC graphs, sensitivity/specificity curves, lift charts, and
    precision/recall plots are popular examples of trade-off visualizations for
    specific pairs of performance measures. ROCR is a flexible tool for
    creating cutoff-parameterized 2D performance curves by freely combining two
    from over 25 performance measures (new performance measures can be added
    using a standard interface).  Curves from different cross-validation or
    bootstrapping runs can be averaged by different methods, and standard
    deviations, standard errors or box plots can be used to visualize the
    variability across the runs. The parameterization can be visualized by
    printing cutoff values at the corresponding curve positions, or by coloring
    the curve according to cutoff. All components of a performance plot can be
    quickly adjusted using a flexible parameter dispatching mechanism. Despite
    its flexibility, ROCR is easy to use, with only three commands and
    reasonable default values for all optional parameters."""

    cran = "ROCR"

    version("1.0-11", sha256="57385a773220a3aaef5b221a68b2d9c2a94794d4f9e9fc3c1eb9521767debb2a")
    version("1.0-7", sha256="e7ef710f847e441a48b20fdc781dbc1377f5a060a5ee635234053f7a2a435ec9")

    depends_on("r@3.6:", type=("build", "run"), when="@1.0-11:")
    depends_on("r-gplots", type=("build", "run"))
