# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQvalue(RPackage):
    """Q-value estimation for false discovery rate control.

    This package takes a list of p-values resulting from the simultaneous
    testing of many hypotheses and estimates their q-values and local FDR
    values. The q-value of a test measures the proportion of false positives
    incurred (called the false discovery rate) when that particular test is
    called significant. The local FDR measures the posterior probability the
    null hypothesis is true given the test's p-value. Various plots are
    automatically generated, allowing one to make sensible significance cut-
    offs. Several mathematical results have recently been shown on the
    conservative accuracy of the estimated q-values from this software. The
    software can be applied to problems in genomics, brain imaging,
    astrophysics, and data mining."""

    bioc = "qvalue"

    version("2.32.0", commit="a6272dc68f9d91de63e04fae28476e4ec016ee89")
    version("2.30.0", commit="e8a4c22d035f860ee730aa7c5a4dbc7460afcedc")
    version("2.28.0", commit="aaa62d5ab5a960e0a626928abaf5b3a5c5f73374")
    version("2.26.0", commit="6d7410d4b8673bcf9065e054670c1fbcb917a27e")
    version("2.22.0", commit="b4bde8198252737b287fd7f9a4ed697f57fad92c")
    version("2.16.0", commit="5efbe20ef522a45a7a04b681f72bb9a12e2747ae")
    version("2.14.1", commit="b694e4b264f25250eb1d1115e70c07f65767c20e")
    version("2.12.0", commit="7df64ebfcbe69dcbf8b88cb6ef0068bf16979673")
    version("2.10.0", commit="581e5664b4356440a96310897398f01a98ceb81b")
    version("2.8.0", commit="c7bf3315619d42d800f57a36670c25a7495ded72")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
