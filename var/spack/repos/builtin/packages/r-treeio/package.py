# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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
