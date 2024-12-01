# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgpubr(RPackage):
    """'ggplot2' Based Publication Ready Plots.

    The 'ggplot2' package is excellent and flexible for elegant data
    visualization in R. However the default generated plots requires some
    formatting before we can send them for publication. Furthermore, to
    customize a 'ggplot', the syntax is opaque and this raises the level of
    difficulty for researchers with no advanced R programming skills. 'ggpubr'
    provides some easy-to-use functions for creating and customizing 'ggplot2'-
    based publication ready plots."""

    cran = "ggpubr"

    license("GPL-2.0-or-later")

    version("0.6.0", sha256="2e6ec5d8151991d17ef8832259cf545fa0d1a50b326ba8c1c4657700171df774")
    version("0.4.0", sha256="abb21ec0b1ae3fa1c58eedca2d59b9b009621b30e3660f1247b3880c5fa50675")
    version("0.2.2", sha256="1c93dc6d1f08680dd00a10b6842445700d1fccb11f18599fbdf51e70c6b6b364")
    version("0.2.1", sha256="611e650da9bd15d7157fdcdc4e926fee3b88df3aba87410fdb1c8a7294d98d28")
    version("0.2", sha256="06c3075d8c452840662f5d041c3d966494b87254a52a858c849b9e1e96647766")
    version("0.1.2", sha256="9b4749fe1a6e0e4c5201a587c57c1b4bed34253f95ab4fb365f7e892b86003fe")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-ggplot2@3.4.0:", type=("build", "run"), when="@0.6.0:")
    depends_on("r-ggrepel", type=("build", "run"))
    depends_on("r-ggrepel@0.9.2:", type=("build", "run"), when="@0.6.0:")
    depends_on("r-ggsci", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"), when="@0.2:")
    depends_on("r-tidyr@1.3.0:", type=("build", "run"), when="@0.6.0:")
    depends_on("r-plyr", type=("build", "run"), when="@:0.1.2")
    depends_on("r-purrr", type=("build", "run"), when="@0.2:")
    depends_on("r-dplyr@0.7.1:", type=("build", "run"), when="@0.2:")
    depends_on("r-cowplot", type=("build", "run"), when="@0.2:")
    depends_on("r-cowplot@1.1.1:", type=("build", "run"), when="@0.6.0:")
    depends_on("r-ggsignif", type=("build", "run"), when="@0.2:")
    depends_on("r-scales", type=("build", "run"), when="@0.2:")
    depends_on("r-gridextra", type=("build", "run"), when="@0.2:")
    depends_on("r-glue", type=("build", "run"), when="@0.2:")
    depends_on("r-polynom", type=("build", "run"), when="@0.2:")
    depends_on("r-rlang", type=("build", "run"), when="@0.2.2:")
    depends_on("r-rlang@0.4.6:", type=("build", "run"), when="@0.6.0:")
    depends_on("r-rstatix@0.6.0:", type=("build", "run"), when="@0.4.0:")
    depends_on("r-rstatix@0.7.2:", type=("build", "run"), when="@0.6.0:")
    depends_on("r-tibble", type=("build", "run"), when="@0.4.0:")
    depends_on("r-magrittr", type=("build", "run"))
