# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAcgh(RPackage):
    """Classes and functions for Array Comparative Genomic Hybridization data.

    Functions for reading aCGH data from image analysis output files and
    clone information files, creation of aCGH S3 objects for storing these
    data. Basic methods for accessing/replacing, subsetting, printing and
    plotting aCGH objects."""

    bioc = "aCGH"

    version("1.78.0", commit="75df3a4839af66ce177d1bbc3cec4ac03c21dc8e")
    version("1.76.0", commit="c6068522854ed0b1c3feb006619ef25590f70ad6")
    version("1.74.0", commit="e7ba380af0da138788eb6c86f5dbe453269c0810")
    version("1.72.0", commit="b5d4022ac487125194d3913f1b8c2948db6e2792")
    version("1.68.0", commit="91f41a3917ddce43eb05e11c90eb99c467ba2247")
    version("1.62.0", commit="3b68b69c3380fa3b66dfb060457628a4a9c22d4f")
    version("1.60.0", commit="ae581758aaa1755448f0cfef5adfb30d1e820b21")
    version("1.58.0", commit="2decc79a21bff5a14d708cdc654e351515b20d3e")
    version("1.56.0", commit="f3531ec99fc181044bdcb6a01c9976029efb6235")
    version("1.54.0", commit="be2ed339449f55c8d218e10c435e4ad356683693")

    depends_on("cxx", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-cluster", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-multtest", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
