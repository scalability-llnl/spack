# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RInfluencer(RPackage):
    """Software Tools to Quantify Structural Importance of Nodes in a Network.

    Provides functionality to compute various node centrality measures on
    networks. Included are functions to compute betweenness centrality (by
    utilizing Madduri and Bader's SNAP library), implementations of Burt's
    constraint and effective network size (ENS) metrics, Borgatti's algorithm
    to identify key players, and Valente's bridging metric. On Unix systems,
    the betweenness, Key Players, and bridging implementations are parallelized
    with OpenMP, which may run faster on systems which have OpenMP
    configured."""

    cran = "influenceR"

    version("0.1.5", sha256="8164e4820f769032fab97c9ca486d33e83309641fcc4875065d8f5a43b20f58c")
    version("0.1.0.1", sha256="63c46f1175fced33fb1b78d4d56e37fbee09b408945b0106dac36e3344cd4766")
    version("0.1.0", sha256="4fc9324179bd8896875fc0e879a8a96b9ef2a6cf42a296c3b7b4d9098519e98a")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-igraph@1.0.1:", type=("build", "run"))
    depends_on("r-matrix@1.1-4:", type=("build", "run"))
