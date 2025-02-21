# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQuickplot(RPackage):
    """A System of Plotting Optimized for Speed and Modularity.

    A high-level plotting system, built using 'grid' graphics, that is
    optimized for speed and modularity. This has great utility for quick
    visualizations when testing code, with the key benefit that visualizations
    are updated independently of one another."""

    cran = "quickPlot"

    maintainers("dorton21")

    version("1.0.2", sha256="78b19e03f9925ea3a5b47c12fef58a154dc0d3598dbdda3fe4e47c6636ab4808")
    version("0.1.8", sha256="5927186ebbd86d2282c59dd28c4af6977ae5f9bc5766de8fce34b94bbfe33be7")
    version("0.1.6", sha256="48690a77ae961ed1032130621ef06b2eaf86ee592bf1057471a8c6d6a98ace55")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r@4.0:", type=("build", "run"), when="@0.1.8:")
    depends_on("r@4.1:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-data-table@1.10.4:", type=("build", "run"))
    depends_on("r-fpcompare", type=("build", "run"))
    depends_on("r-terra", type=("build", "run"), when="@1.0.1:")

    depends_on("r-backports", type=("build", "run"), when="@:1.0.1")
    depends_on("r-ggplot2", type=("build", "run"), when="@:1.0.1")
    depends_on("r-gridbase", type=("build", "run"), when="@:1.0.1")
    depends_on("r-igraph", type=("build", "run"), when="@:1.0.1")
    depends_on("r-raster", type=("build", "run"), when="@:1.0.1")
    depends_on("r-rcolorbrewer", type=("build", "run"), when="@:1.0.1")
    depends_on("r-rgdal", type=("build", "run"), when="@:1.0.1")
    depends_on("r-rgeos", type=("build", "run"), when="@:1.0.1")
    depends_on("r-sp", type=("build", "run"), when="@:1.0.1")
