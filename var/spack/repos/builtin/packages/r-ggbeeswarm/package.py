# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgbeeswarm(RPackage):
    """Categorical Scatter (Violin Point) Plots.

    Provides two methods of plotting categorical scatter plots such that the
    arrangement of points within a category reflects the density of data at
    that region, and avoids over-plotting."""

    cran = "ggbeeswarm"

    license("GPL-3.0-or-later")

    version("0.7.2", sha256="fd7ca265bb892dde514d5f8d6a853fb8b32d7a673b05e9c8b50544a523299ce5")
    version("0.7.1", sha256="f41550335149bc2122fed0dd280d980cecd02ace79e042d5e03c1f102200ac92")
    version("0.6.0", sha256="bbac8552f67ff1945180fbcda83f7f1c47908f27ba4e84921a39c45d6e123333")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.7.1:")
    depends_on("r-beeswarm", type=("build", "run"))
    depends_on("r-cli", type=("build", "run"), when="@0.7.2:")
    depends_on("r-lifecycle", type=("build", "run"), when="@0.7.1:")
    depends_on("r-ggplot2@2.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.3.0:", type=("build", "run"), when="@0.7.1:")
    depends_on("r-vipor", type=("build", "run"))
