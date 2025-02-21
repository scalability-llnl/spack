# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIgraph(RPackage):
    """Network Analysis and Visualization.

    Routines for simple graphs and network analysis. It can handle large graphs
    very well and provides functions for generating random and regular graphs,
    graph visualization, centrality methods and much more."""

    cran = "igraph"

    license("GPL-2.0-or-later")

    version("2.0.3", sha256="8e8a172d4567219474562cfb1085496be3ab356483c4e88011aca1fc3b2d8f76")
    version("1.4.2", sha256="7d5300adb1a25a6470cada8630e35ef416181147ab624d5a0a8d3552048c4ae5")
    version("1.3.5", sha256="9e615d67b6b5b57dfa54ec2bbc8c29da8f7c3fe82af1e35ab27273b1035b9bd4")
    version("1.3.1", sha256="505a2ba7c417ceaf869240cc1c9a5f3fbd75f8d9dfcfe048df1326c6ec41144e")
    version("1.2.11", sha256="1c8b715eb61e6e7d9082858673929f8e84dc832c0a2a7aba7811511bbd2000de")
    version("1.2.6", sha256="640da72166fda84bea2c0e5eee374f1ed80cd9439c1171d056b1b1737ae6c76d")
    version("1.2.4.1", sha256="891acc763b5a4a4a245358a95dee69280f4013c342f14dd6a438e7bb2bf2e480")
    version("1.2.4", sha256="1048eb26ab6b592815bc269c1d91e974c86c9ab827ccb80ae0a40042019592cb")
    version("1.1.2", sha256="89b16b41bc77949ea208419e52a18b78b5d418c7fedc52cd47d06a51a6e746ec")
    version("1.0.1", sha256="dc64ed09b8b5f8d66ed4936cde3491974d6bc5178dd259b6eab7ef3936aa5602")

    depends_on("r@3.0.2:", type=("build", "run"), when="@1.4.2:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.5.0:")

    depends_on("r-cli", type=("build", "run"), when="@1.5.0:")
    depends_on("r-cpp11@0.2.0:", type=("build", "run"), when="@1.4.2:")
    depends_on("r-cpp11@0.4.7:", type=("build", "run"), when="@1.6.0:")
    depends_on("r-lifecycle", type=("build", "run"), when="@1.5.0.1:")
    depends_on("r-vctrs", type=("build", "run"), when="@2.0.3:")
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-pkgconfig@2.0.0:", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@1.3.5:")
    depends_on("r-vctrs", type=("build", "run"), when="@2.0.2:")
    depends_on("gmp")
    depends_on("gmp@4.38:", when="@1.2.11:")
    depends_on("libxml2")
    depends_on("glpk", when="@1.2.0:")
    depends_on("glpk@4.57:", when="@1.3.1:")

    depends_on("r-irlba", type=("build", "run"), when="@:1.1.9")
