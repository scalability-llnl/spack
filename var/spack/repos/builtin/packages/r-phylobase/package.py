# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPhylobase(RPackage):
    """Base Package for Phylogenetic Structures and Comparative Data.

    Provides a base S4 class for comparative methods, incorporating one or more
    trees and trait data."""

    cran = "phylobase"

    license("GPL-2.0-or-later")

    version("0.8.12", sha256="9b81ca60dc6215e74b720880cc2db3abc1f7e6d8785ea7d7df95a950f0778f20")
    version("0.8.10", sha256="5a44380ff49bab333a56f6f96157324ade8afb4af0730e013194c4badb0bf94b")

    depends_on("r-ade4", type=("build", "run"))
    depends_on("r-ape@3.0:", type=("build", "run"))
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
    depends_on("r-rncl@0.6.0:", type=("build", "run"))
    depends_on("r-rnexml", type=("build", "run"))
