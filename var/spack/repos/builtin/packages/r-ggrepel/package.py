# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgrepel(RPackage):
    """Repulsive Text and Label Geoms for 'ggplot2'.

    Provides text and label geoms for 'ggplot2' that help to avoid overlapping
    text labels. Labels repel away from each other and away from the data
    points."""

    cran = "ggrepel"

    license("GPL-3.0-only OR custom")

    version("0.9.5", sha256="d1e600e56c2ad345961ed23f30f04b81c631ff94bd6762a260c62e0206cf8caa")
    version("0.9.3", sha256="b9eba0e2edee84db0276b49e4834b65f5369edc4bc56f4cacc13e0d1c39a005c")
    version("0.9.2", sha256="0a3088c48177528e2a65defebbc4f09a744ebb44408588f688811f8d0d827488")
    version("0.9.1", sha256="29fb916d4799ba6503a5dd019717ffdf154d2aaae9ff1736f03e2be24af6bdfc")
    version("0.9.0", sha256="4f7ca3da7dc08902487c961c539ef43516263c30abcc4ce303ff3c5580f42fda")
    version("0.8.1", sha256="d5d03a77ab6d8c831934bc46e840cc4e3df487272ab591fa72767ad42bcb7283")
    version("0.8.0", sha256="6386606e716d326354a29fcb6cd09f9b3d3b5e7c5ba0d5f7ff35416b1a4177d4")
    version("0.6.5", sha256="360ae9d199755f9e260fefbd3baba3448fad3f024f20bcd9942a862b8c41a752")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-ggplot2@2.2.0:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rlang@0.3.0:", type=("build", "run"), when="@0.9.0:")
    depends_on("r-scales@0.3.0:", type=("build", "run"))
    depends_on("r-scales@0.5.0:", type=("build", "run"), when="@0.9.0:")
    depends_on("r-withr@2.5.0:", type=("build", "run"), when="@0.9.3:")
