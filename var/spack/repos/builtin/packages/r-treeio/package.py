# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTreeio(RPackage):
    """Base Classes and Functions for Phylogenetic Tree Input and Output.

    'treeio' is an R package to make it easier to import and store phylogenetic
    tree with associated data; and to link external data from different sources
    to phylogeny. It also supports exporting phylogenetic tree with
    heterogeneous associated data to a single tree file and can be served as a
    platform for merging tree with associated data and converting file
    formats."""

    bioc = "treeio"

    version("1.30.0", commit="c824ca4d2a8a9229922afea60775467905505012")
    version("1.28.0", commit="39ca57b4b2f0528b54fcdb7c0c9c4d28b2603dc0")
    version("1.26.0", commit="cce8f0aa896888bd6116897d08ab54e69c814631")
    version("1.24.0", commit="81425559d71ab87ee683c6a8833f0f165632e416")
    version("1.22.0", commit="eb24a854806a671e7b37ef36dafc60b4eb9ddaa1")
    version("1.20.2", commit="ed457d6fd85a50e0993c8c9acbd9b701be01a348")
    version("1.20.0", commit="5f7c3704fc8202c52451d092148fdcfe683f026a")
    version("1.18.1", commit="a06b6b3d2a64f1b22c6c8c5f97c08f5863349c83")

    depends_on("r@3.6.0:", type=("build", "run"))
    depends_on("r-ape", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-tidytree@0.3.0:", type=("build", "run"))
    depends_on("r-tidytree@0.3.9:", type=("build", "run"), when="@1.20.0:")
    depends_on("r-cli", type=("build", "run"), when="@1.24.0:")
