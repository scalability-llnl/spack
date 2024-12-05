# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFgsea(RPackage):
    """Fast Gene Set Enrichment Analysis.

    The package implements an algorithm for fast gene set enrichment
    analysis. Using the fast algorithm allows to make more permutations and
    get more fine grained p-values, which allows to use accurate stantard
    approaches to multiple hypothesis correction."""

    bioc = "fgsea"

    license("MIT")

    version("1.26.0", commit="102b439e2208ae415dc19d3d1ac8936f9c5999f1")
    version("1.24.0", commit="ac74ccd935c15623b8584caa791835aec514144b")
    version("1.22.0", commit="e4e203aa64faa984e0406fed5d87a422d9df92f2")
    version("1.20.0", commit="b704f81687dc16afdaafc6d30108c62a067856b2")
    version("1.16.0", commit="9d9df596c7e160afa18e067b7637cfc465494318")
    version("1.10.1", commit="fb06a6ebfb4a195e77e37226d100a2148b90c5f3")
    version("1.8.0", commit="bb2898aca9fb23e90770671a83fe23f79bb1841b")
    version("1.6.0", commit="52b801b7c2dfd8238fa8f2b402fddb4fda60271d")
    version("1.4.1", commit="73de5ff364e520ac99507a9ee5a61a0d23d3c44e")
    version("1.2.1", commit="99b04eef664204d0dca4b9f8027cd7eefb006b72")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"))
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-ggplot2@2.2.0:", type=("build", "run"))
    depends_on("r-cowplot", type=("build", "run"), when="@1.24.0:")
    depends_on("r-fastmatch", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"), when="@1.6.0:")
    depends_on("r-scales", type=("build", "run"), when="@1.26.0:")
    depends_on("r-bh", type=("build", "run"), when="@1.10.1:")

    depends_on("r-gridextra", type=("build", "run"), when="@:1.22.0")
