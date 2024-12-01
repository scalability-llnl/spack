# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBluster(RPackage):
    """Clustering Algorithms for Bioconductor.

    Wraps common clustering algorithms in an easily extended S4 framework.
    Backends are implemented for hierarchical, k-means and graph-based
    clustering.  Several utilities are also provided to compare and evaluate
    clustering results."""

    bioc = "bluster"

    version("1.10.0", commit="32340420e67a184e39238e46143c00151057924c")
    version("1.8.0", commit="156115c8960c0b66b2c588d9fd8bbdfe56e5f0be")
    version("1.6.0", commit="ff86c7d8d36233e838d4f00e6a4e173e7bf16816")

    depends_on("cxx", type="build")  # generated

    depends_on("r-cluster", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-igraph", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-biocneighbors", type=("build", "run"))
