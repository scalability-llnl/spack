# Copyright Spack Project Developers. See COPYRIGHT file for details.
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

    version("1.16.0", commit="32aa5ea9e7595959119e555e26034a4e95338b32")
    version("1.14.0", commit="5b73704f633882a8f4e26ccd8b516c719361d9f2")
    version("1.12.0", commit="efc4220a8062cab433a89d3d742880128cdcaad2")
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
    depends_on("r-assorthead", type=("build", "run"), when="@1.15.1:")
