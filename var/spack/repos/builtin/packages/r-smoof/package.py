# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSmoof(RPackage):
    """Single and Multi-Objective Optimization Test Functions.

    Provides generators for a high number of both single- and multi- objective
    test functions which are frequently used for the benchmarking of
    (numerical) optimization algorithms. Moreover, it offers a set of
    convenient functions to generate, plot and work with objective
    functions."""

    cran = "smoof"

    license("BSD-2-Clause")

    version("1.6.0.3", sha256="af8664b152876c545f6545528de6e05a289d0714103fac7afc52960a9a855fb1")
    version("1.6.0.2", sha256="d82dba9702eade00afb84c2c12167de6cec790be7d23ac227f8fe705bdcefc93")
    version("1.5.1", sha256="cfb6f6460e9593351428656b225b5ba3867a216d35a05f2babdb20db6ba35306")
    version("1.5", sha256="9b73ad5bfc8e1120c9651539ea52b1468f316cc7fc5fef8afd6d357adf01504c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r+X", type=("build", "run"))
    depends_on("r-paramhelpers@1.8:", type=("build", "run"))
    depends_on("r-checkmate@1.1:", type=("build", "run"))
    depends_on("r-bbmisc@1.6:", type=("build", "run"))
    depends_on("r-ggplot2@2.2.1:", type=("build", "run"))
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
    depends_on("r-rcpparmadillo", type=("build", "run"))
    depends_on("r-mco", type=("build", "run"), when="@:1.6.0.2")
    depends_on("r-plot3d", type=("build", "run"), when="@:1.6.0.2")
    depends_on("r-plotly", type=("build", "run"), when="@:1.6.0.2")
    depends_on("r-rcolorbrewer", type=("build", "run"), when="@:1.6.0.2")
    depends_on("r-rjsonio", type=("build", "run"), when="@:1.6.0.2")
