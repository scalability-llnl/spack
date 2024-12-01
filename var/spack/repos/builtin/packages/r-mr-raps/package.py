# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMrRaps(RPackage):
    """Two Sample Mendelian Randomization using Robust Adjusted Profile Score.

    Mendelian randomization is a method of identifying and estimating a
    confounded causal effect using genetic instrumental variables. This
    packages implements methods for two-sample Mendelian randomization with
    summary statistics by using Robust Adjusted Profile Score (RAPS).
    References: Qingyuan Zhao, Jingshu Wang, Jack Bowden, Dylan S. Small.
    Statistical inference in two-sample summary-data Mendelian randomization
    using robust adjusted profile score. <arXiv:1801.09652>."""

    cran = "mr.raps"

    version("0.2", sha256="c899f6143dac99e1232ff0a8d9f5fe099d4f69960782e6843db5b0d7f4f63b19")

    depends_on("r-nortest", type=("build", "run"))
