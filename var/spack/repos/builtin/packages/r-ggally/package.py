# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgally(RPackage):
    """Extension to 'ggplot2'.

    The R package 'ggplot2' is a plotting system based on the grammar of
    graphics. 'GGally' extends 'ggplot2' by adding several functions to reduce
    the complexity of combining geometric objects with transformed data. Some
    of these functions include a pairwise plot matrix, a two group pairwise
    plot matrix, a parallel coordinates plot, a survival plot, and several
    functions to plot networks."""

    cran = "GGally"

    version("2.2.1", sha256="8bb326665936a63f6eef92a2af1a11d1fae78dbd28d6980608d2b38ee1f586c6")
    version("2.1.2", sha256="30352f36bf061bc98bdd5fa373ea0f23d007040bd908c7c018c8e627e0fb28e5")
    version("2.1.0", sha256="7ffb86b8a4e79543cf7e6bb1e3684d738ecd8e0ba89e8ef38991898b18dd6c53")
    version("1.4.0", sha256="9a47cdf004c41f5e4024327b94227707f4dad3a0ac5556d8f1fba9bf0a6355fe")
    version("1.3.2", sha256="f4143f45254fed794be991180aeffe459f6756bfa08acad963707d8e843cfd0a")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r-ggplot2@2.2.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.3.0:", type=("build", "run"), when="@2.1.0:")
    depends_on("r-ggplot2@3.3.4:", type=("build", "run"), when="@2.1.2:")
    depends_on("r-ggplot2@3.4.4:", type=("build", "run"), when="@2.2.0:")
    depends_on("r-dplyr@1.0.0:", type=("build", "run"), when="@2.1.0:")
    depends_on("r-ggstats", type=("build", "run"), when="@2.2.0:")
    depends_on("r-gtable@0.2.0:", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@2.1.0:")
    depends_on("r-plyr@1.8.3:", type=("build", "run"))
    depends_on("r-progress", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@1.4.0:")
    depends_on("r-scales@1.1.0:", type=("build", "run"), when="@2.1.0:")
    depends_on("r-tidyr", type=("build", "run"), when="@2.1.0:")
    depends_on("r-tidyr@1.3.0:", type=("build", "run"), when="@2.2.0:")
    depends_on("r-magrittr", type=("build", "run"), when="@2.2.0:")
    depends_on("openssl", when="@1.4.0:")

    depends_on("r-forcats", type=("build", "run"), when="@2.1.0:2.1")
    depends_on("r-reshape@0.8.5:", type=("build", "run"), when="@:2.1")
