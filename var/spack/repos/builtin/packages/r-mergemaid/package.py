# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMergemaid(RPackage):
    """Merge Maid.

    The functions in this R extension are intended for cross-study
    comparison of gene expression array data. Required from the user is gene
    expression matrices, their corresponding gene-id vectors and other
    useful information, and they could be 'list','matrix', or
    'ExpressionSet'. The main function is 'mergeExprs' which transforms the
    input objects into data in the merged format, such that common genes in
    different datasets can be easily found. And the function 'intcor'
    calculate the correlation coefficients. Other functions use the output
    from 'modelOutcome' to graphically display the results and cross-
    validate associations of gene expression data with survival."""

    bioc = "MergeMaid"

    version("2.56.0", commit="c510d1d85bb39476e8397b24c4bc127780a17686")
    version("2.54.0", commit="8e79bd2bd06b25138b3c5107681c89d714a3b194")
    version("2.52.0", commit="88a1ddfd9cdbe902ba40fae0f39ee5665ac33a74")
    version("2.50.0", commit="b77d7fcb8ac8cf9ee71303bb193ef1a36a7f6049")
    version("2.48.0", commit="aee89c523fcafff4c166ff3db4fff90df16a1ed4")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
